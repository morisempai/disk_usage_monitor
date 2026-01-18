import datetime
from scipy.spatial import KDTree
import asyncio
import logging

from canvas.canvas import Canvas, QueueElement, ObjActions
from engine.obsticle import Obsticle
from engine.particle import Particle
from engine.utils import rotate

logger = logging.getLogger()

class SimpleColisionEngine():
    def __init__(self, particles: list[Particle], obsticles: list[Obsticle]=[], radius=30, boundaries=300, prerendered_frames=1000, fps=30):
        self.g = 9.8
        self.particles = []
        self.particles_to_create = particles
        self.particles_to_delete = [] # To delete particles only after it was get

        self.obsticles = obsticles
        self.last_frame_time = datetime.datetime.now()
        self.radius = radius
        self.boudaries = boundaries

        self.frames = [] #TODO rewrite with normal queue
        self.prerendered_frames = prerendered_frames
        self.fps = fps

    
    def start(self):
        pass 

    def loop(self):
        pass

    def register_canvas(self, canvas: Canvas):
        self.canvas = canvas(self.frames)

    async def start_engine_async(self):
        generate_task = asyncio.create_task(self.genearate_frame())
        get_frame_task = asyncio.create_task(self.canvas.draw()) 
        await asyncio.gather(generate_task, get_frame_task)

    def run(self):
        self.start()
        asyncio.run(self.start_engine_async())
        
    async def genearate_frame(self):
        while True:
            if len(self.frames) > self.prerendered_frames:
                logger.info("List of prerendered frames is full")
                await asyncio.sleep(self.prerendered_frames/self.fps/2)
            self.loop()
            self.update()
            frame = {}
            # Add deleting particles (need to create async task that tracks deleting object and deletes them after ensuring it is not in use anymore)
            for p in self.particles:
                frame[p.id] = QueueElement(p.x, p.y, p.radius, action=ObjActions.MOVE)
            for p in self.particles_to_create:
                frame[p.id] = QueueElement(p.x, p.y, p.radius, action=ObjActions.CREATE)
                self.particles_to_create.remove(p)
                self.particles.append(p)
            for p in self.particles_to_delete:
                frame[p.id] = QueueElement(p.x, p.y, p.radius, action=ObjActions.DELETE)
                self.particles_to_delete.remove(p)
                self.particles.remove(p)
            self.frames.append(frame)

    def add_particle(self, particle: Particle):
        self.particles_to_create.append(particle)

    def delete_particle(self, particle: Particle):
        self.particles_to_delete.append(particle)

    def obsticle_collision(self):
        for particle in self.particles:
            for obsticle in self.obsticles:
                x, y = rotate(particle.x, particle.y, obsticle.sin_coof, obsticle.cos_coof)
                x_distance = abs(x - obsticle.rotated_middle_x)
                y_distance = abs(y - obsticle.rotated_middle_y)
                availible_space_y =  particle.radius + obsticle.lengh/2
                availible_space_x =  particle.radius
                if x_distance < availible_space_x and y_distance < availible_space_y:
                    # For bouncing effect
                    # TODO move particles back so that they do not overlap
                    particle.x, particle.y = rotate(-particle.radius + obsticle.rotated_middle_x, y, obsticle.sin_coof, obsticle.cos_coof, clockwise=True)
                    x_velocity_r, y_velocity_r = rotate(particle.velocity_x, particle.velocity_y, obsticle.sin_coof, obsticle.cos_coof)
                    x_velocity, y_velocity = rotate(-x_velocity_r*obsticle.friction, y_velocity_r, obsticle.sin_coof, obsticle.cos_coof, clockwise=True)
                    particle.velocity_x = (x_velocity)
                    particle.velocity_y = (y_velocity)

    def compute_collision(self, particle1: Particle, particle2: Particle):
        # Turn speed vector by collision angle, exchange speed by y coord, turn back
        delta_x = particle1.x-particle2.x
        delta_y = particle1.y-particle2.y
        length = (abs(delta_x)**2 + abs(delta_y)**2)**0.5
        sin_coof = delta_x / length
        cos_coof = delta_y / length
        # Moving particles back so that they do not overlap
        rotated_x1, rotated_y1 = rotate(particle1.x, particle1.y, sin_coof, cos_coof)
        rotated_x2, rotated_y2 = rotate(particle2.x, particle2.y, sin_coof, cos_coof)
        intersection_y = abs(rotated_y1 - rotated_y2) - self.radius
        particle1.x, particle1.y = rotate(rotated_x1, rotated_y1-intersection_y/2, sin_coof, cos_coof, clockwise=True)
        particle2.x, particle2.y = rotate(rotated_x2, rotated_y2+intersection_y/2, sin_coof, cos_coof, clockwise=True)
        # Bouncing effect
        rotated_v_x1, rotated_v_y1 = rotate(particle1.velocity_x, particle1.velocity_y, sin_coof, cos_coof)
        rotated_v_x2, rotated_v_y2 = rotate(particle2.velocity_x, particle2.velocity_y, sin_coof, cos_coof)
        friction = particle1.friction * particle2.friction
        rotated_v_y2, rotated_v_y1 = rotated_v_y1 * friction * particle1.mass / particle2.mass, rotated_v_y2 * friction * particle2.mass / particle1.mass
        particle1.velocity_x, particle1.velocity_y = rotate(rotated_v_x1, rotated_v_y1, sin_coof, cos_coof, clockwise=True)
        particle2.velocity_x, particle2.velocity_y = rotate(rotated_v_x2, rotated_v_y2, sin_coof, cos_coof, clockwise=True)
    
    def particle_collision(self):
        # Fix 2 for loop (with quadtrees?)
        for index1, particle1 in enumerate(self.particles[0:-1]):
            for _, particle2 in enumerate(self.particles[1+index1::]):
                x_distance = abs(particle1.x - particle2.x)
                y_distance = abs(particle1.y - particle2.y)
                min_space = particle1.radius + particle2.radius
                if x_distance < min_space and y_distance < min_space:
                    self.compute_collision(particle1, particle2)        

    def obsticle_collision_kdtree(self):
        particles = [(p.x, p.y) for p in self.particles]
        tree = KDTree(particles)
        for obsticle in self.obsticles:
            collisions = tree.query_ball_point((obsticle.middle_x, obsticle.middle_y), r=obsticle.lengh/2)
            particles = [self.particles[i] for i in collisions]
            for particle in particles:
                x, y = rotate(particle.x, particle.y, obsticle.sin_coof, obsticle.cos_coof)
                x_distance = abs(x - obsticle.rotated_middle_x)
                y_distance = abs(y - obsticle.rotated_middle_y)
                availible_space_y =  particle.radius + obsticle.lengh/2
                availible_space_x =  particle.radius
                if x_distance < availible_space_x and y_distance < availible_space_y:
                    # For bouncing effect
                    particle.x, particle.y = rotate(-particle.radius + obsticle.rotated_middle_x, y, obsticle.sin_coof, obsticle.cos_coof, clockwise=True)
                    x_velocity_r, y_velocity_r = rotate(particle.velocity_x, particle.velocity_y, obsticle.sin_coof, obsticle.cos_coof)
                    x_velocity, y_velocity = rotate(-x_velocity_r*obsticle.friction, y_velocity_r, obsticle.sin_coof, obsticle.cos_coof, clockwise=True)
                    particle.velocity_x = (x_velocity)
                    particle.velocity_y = (y_velocity)
        pass
    
    def particle_collision_kdtree(self):
        particles = [(p.x, p.y) for p in self.particles]
        tree = KDTree(particles)
        pairs = tree.query_pairs(self.radius)
        for pair in pairs:
            self.compute_collision(self.particles[pair[0]], self.particles[pair[1]])

    def update(self):
        if not self.particles:
            return
        delta_time = 1/10
        for particle in self.particles:
            if particle.y < -self.boudaries or particle.y > self.boudaries:
                self.delete_particle(particle)
                continue
            particle.x += particle.velocity_x * delta_time
            particle.y += particle.velocity_y * delta_time
            particle.velocity_y -= self.g * delta_time
        self.obsticle_collision_kdtree()
        self.particle_collision_kdtree()