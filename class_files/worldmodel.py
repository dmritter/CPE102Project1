import entities
import pygame
import ordered_list
import actions
import occ_grid
import point

class WorldModel:
   def __init__(self, num_rows, num_cols, background):
      self.background = occ_grid.Grid(num_cols, num_rows, background)
      self.num_rows = num_rows
      self.num_cols = num_cols
      self.occupancy = occ_grid.Grid(num_cols, num_rows, None)
      self.entities = []
      self.action_queue = ordered_list.OrderedList()


   def within_bounds(self, pt):
      return (pt.x >= 0 and pt.x < self.num_cols and
         pt.y >= 0 and pt.y < self.num_rows)


def is_occupied(world, pt):
   return (world.within_bounds(pt) and
      world.occupancy.get_cell(pt) != None)


def nearest_entity(entity_dists):
   if len(entity_dists) > 0:
      pair = entity_dists[0]
      for other in entity_dists:
         if other[1] < pair[1]:
            pair = other
      nearest = pair[0]
   else:
      nearest = None

   return nearest


def distance_sq(p1, p2):
   return (p1.x - p2.x)**2 + (p1.y - p2.y)**2


def find_nearest(world, pt, type):
   oftype = [(e, distance_sq(pt, entities.get_position(e)))
      for e in world.entities if isinstance(e, type)]

   return nearest_entity(oftype)


def add_entity(world, entity):
   pt = entities.get_position(entity)
   if world.within_bounds(pt):
      old_entity = world.occupancy.get_cell(pt)
      if old_entity != None:
         entities.clear_pending_actions(old_entity)
      world.occupancy.set_cell(pt, entity)
      world.entities.append(entity)


def move_entity(world, entity, pt):
   tiles = []
   if world.within_bounds(pt):
      old_pt = entities.get_position(entity)
      world.occupancy.set_cell(old_pt, None)
      tiles.append(old_pt)
      world.occupancy.set_cell(pt, entity)
      tiles.append(pt)
      entities.set_position(entity, pt)

   return tiles


def remove_entity(world, entity):
   remove_entity_at(world, entities.get_position(entity))


def remove_entity_at(world, pt):
   if (world.within_bounds(pt) and
      world.occupancy.get_cell(pt) != None):
      entity = world.occupancy.get_cell(pt)
      entities.set_position(entity, point.Point(-1, -1))
      world.entities.remove(entity)
      world.occupancy.set_cell(pt, None)


def schedule_action(world, action, time):
   world.action_queue.insert(action, time)


def unschedule_action(world, action):
   world.action_queue.remove(action)


def update_on_time(world, ticks):
   tiles = []

   next = world.action_queue.head()
   while next and next.ord < ticks:
      world.action_queue.pop()
      tiles.extend(next.item(ticks))  # invoke action function
      next = world.action_queue.head()

   return tiles


def get_background_image(world, pt):
   if world.within_bounds(pt):
      return entities.get_image(world.background.get_cell(pt))


def get_background(world, pt):
   if world.within_bounds(pt):
      return world.background.get_cell(pt)


def set_background(world, pt, bgnd):
   if world.within_bounds(pt):
      world.background.set_cell(pt, bgnd)


def get_tile_occupant(world, pt):
   if world.within_bounds(pt):
      return world.occupancy.get_cell(pt)


def get_entities(world):
   return world.entities
