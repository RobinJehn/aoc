from dataclasses import dataclass
from copy import copy, deepcopy

@dataclass
class Point:
	x: int
	y: int
	z: int

	def get_fall_down_one_step(self):
		return Point(self.x, self.y, self.z-1)


class Brick:
	def __init__(self, start: Point, finish: Point) -> None:
		self.start: Point = start
		self.finish: Point = finish
		self.blocks: list[Point] = []

		for i in range(self.start.x, self.finish.x+1):
			for j in range(self.start.y, self.finish.y+1):
				for k in range(self.start.z, self.finish.z+1):
					self.blocks.append(Point(i, j, k))

	
	def get_fall_down_one_step(self):
		return Brick(self.start.get_fall_down_one_step(), self.finish.get_fall_down_one_step())
	
	def fall_down_one_step(self):
		other = self.get_fall_down_one_step()
		self.start = other.start
		self.finish = other.finish
		self.blocks = other.blocks


class Space:
	GROUND = 1000000000000000

	def __init__(self, bricks: list[Brick]) -> None:
		self.bricks = bricks
		self.max_x = 0
		self.max_y = 0
		self.max_z = 0

		for b in self.bricks:
			self.max_x = max(self.max_x, b.start.x)
			self.max_x = max(self.max_x, b.finish.x)

			self.max_y = max(self.max_y, b.start.y)
			self.max_y = max(self.max_y, b.finish.y)

			self.max_z = max(self.max_z, b.start.z)
			self.max_z = max(self.max_z, b.finish.z)

		self.blocks: list[list[list[int]]] = [[[-1 for z in range(self.max_z+1)] for y in range(self.max_y+1)] for x in range(self.max_x+1)]
		for i in range(len(self.bricks)):
			brick = self.bricks[i]
			for b in brick.blocks:
				self.blocks[b.x][b.y][b.z] = i

		for x in range(self.max_x+1):
			for y in range(self.max_y+1):
				self.blocks[x][y][0] = Space.GROUND

	def is_free_space(self, brick: Brick, exclude: int) -> bool:
		for b in brick.blocks:
			block_id = self.blocks[b.x][b.y][b.z]
			if block_id != -1 and block_id != exclude:
				return False
		return True

		
def can_disintegrate(bricks: list[Brick]) -> bool:
	s = Space(bricks)
	for i in range(len(bricks)):
		brick = bricks[i]
		brick_before = brick.get_fall_down_one_step()
		if s.is_free_space(brick_before, i ):
			return False
	return True


def fall(bricks: list[Brick]) -> list[Brick]:
	has_fallen = True
	while has_fallen:
		has_fallen = False
		s = Space(bricks)
		for i in range(len(bricks)):
			brick = bricks[i]
			brick_before = brick.get_fall_down_one_step()
			if s.is_free_space(brick_before, i):
				brick.fall_down_one_step()
				has_fallen = True
				continue


def fall_count(bricks: list[Brick]) -> int:
	fallen_indexes = set()
	has_fallen = True
	while has_fallen:
		has_fallen = False
		s = Space(bricks)
		for i in range(len(bricks)):
			brick = bricks[i]
			brick_before = brick.get_fall_down_one_step()
			if i == 99:
				print('here')
			if s.is_free_space(brick_before, i):
				brick.fall_down_one_step()
				has_fallen = True
				fallen_indexes.add(i)
				continue
	return len(fallen_indexes)
	

def task1(bricks: list[Brick]) -> int:
	count = 0
	for i in range(len(bricks)):
		print(i)
		bricks_copy = deepcopy(bricks)
		del bricks_copy[i]
		if can_disintegrate(bricks_copy):
			print(i)
			count += 1
	return count


def task2(bricks: list[Brick]) -> int:
	count = 0
	for i in range(len(bricks)):
		bricks_copy = deepcopy(bricks)
		del bricks_copy[i]
		new_fall_count = fall_count(bricks_copy)
		print(i, new_fall_count)
		count += new_fall_count
	return count


def parse_point(s: str) -> Point:
	x, y, z = [int(l) for l in s.split(',')]
	return Point(x, y, z)


bricks = []
with open('2023/day_22/input.txt', 'r') as file:
	for line in file.readlines():
		start, finish = line.strip().split('~')
		bricks.append(Brick(parse_point(start), parse_point(finish)))


fall(bricks)
count = task2(bricks)

print('Count:')
print(count)