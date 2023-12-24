from shared import BaseChallenge


class Block:
    block_id = 0

    @classmethod
    @property
    def _next_id(cls) -> int:
        cls.block_id += 1
        return cls.block_id

    @classmethod
    def from_line(cls, line: str) -> "Block":
        min_pos, max_pos = line.split("~")
        min_pos = tuple(int(pos) for pos in min_pos.split(","))
        max_pos = tuple(int(pos) for pos in max_pos.split(","))
        return cls(min_pos, max_pos)

    def __init__(
        self,
        min_pos: tuple[int, int, int],
        max_pos: tuple[int, int, int],
        block_id: int | None = None,
    ):
        self.id = self._next_id if block_id is None else block_id
        self.min_x, self.min_y, self.min_z = min_pos
        self.max_x, self.max_y, self.max_z = max_pos

    @property
    def x_range(self) -> range:
        return range(self.min_x, self.max_x + 1)

    @property
    def y_range(self) -> range:
        return range(self.min_y, self.max_y + 1)

    @property
    def z_range(self) -> range:
        return range(self.min_z, self.max_z + 1)

    def move(self, x: int = 0, y: int = 0, z: int = 0) -> "Block":
        self.min_x += x
        self.min_y += y
        self.min_z += z
        self.max_x += x
        self.max_y += y
        self.max_z += z
        return self

    def move_down(self) -> "Block":
        if self.min_z == 1:
            raise ValueError("Block already on the ground")
        return self.move(z=-1)

    def move_up(self) -> "Block":
        return self.move(z=1)

    def intersects(self, other: "Block") -> bool:
        return (
            other.min_x <= self.max_x
            and other.max_x >= self.min_x
            and other.min_y <= self.max_y
            and other.max_y >= self.min_y
            and other.min_z <= self.max_z
            and other.max_z >= self.min_z
        )

    def __contains__(self, other: "Block") -> bool:
        return (
            self.min_x <= other.min_x <= self.max_x
            and self.min_y <= other.min_y <= self.max_y
            and self.min_z <= other.min_z <= self.max_z
        )

    def __repr__(self) -> str:
        return f"Block(id={self.id},min=({self.min_x},{self.min_y},{self.min_z}),max=({self.max_x},{self.max_y},{self.max_z}))"


class Node:
    def __init__(self, node_id: int):
        self.id = node_id
        self.children: set[Node] = set()
        self.parents: set[Node] = set()
        self.destroyed = False

    def _destroy(self) -> int:
        if all(parent.destroyed for parent in self.parents):
            self.destroyed = True
            return 1 + sum((child._destroy() for child in self.children), 0)
        return 0

    def destroy(self) -> int:
        self.destroyed = True
        return sum((child._destroy() for child in self.children), 0)

    def __repr__(self) -> str:
        return f"Node(id={self.id},destroyed={self.destroyed})"

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.id == other.id


class Challenge22(BaseChallenge):
    def __init__(self, steps: int = 64):
        super().__init__()
        self.blocks: list[Block] = []

    def _inside_grid(self, x: int, y: int) -> bool:
        """
        Check if the given position is inside the grid.
        """
        if len(self.blocks) == 0:
            return False
        return 0 <= x < len(self.blocks[0]) and 0 <= y < len(self.blocks)

    def first(self):
        """ """
        self.blocks = list(map(Block.from_line, self.stripped_lines))
        self.blocks.sort(key=lambda block: block.min_z)
        obstacles = sorted(
            self.blocks,
            key=lambda block: block.max_x,
        )

        unremovable_blocks = set()
        for block in self.blocks:
            if block.min_z == 1:
                continue
            found_obstacle = False
            while block.min_z > 1 and not found_obstacle:
                block.move_down()
                base = []
                for obstacle in [
                    ob
                    for ob in obstacles
                    if ob.max_z == block.min_z and ob.id != block.id
                ]:
                    if obstacle.intersects(block):
                        found_obstacle = True
                        base.append(obstacle)
                if found_obstacle:
                    block.move_up()
                    if len(base) == 1:
                        unremovable_blocks.add(base[0])
                    break
        return len(self.blocks) - len(unremovable_blocks)

    def second(self):
        """ """
        self.blocks = list(map(Block.from_line, self.stripped_lines))
        self.blocks.sort(key=lambda block: block.min_z)
        obstacles = sorted(
            self.blocks,
            key=lambda block: block.max_x,
        )

        dependency_tree: dict[int, Node] = {}
        for block in self.blocks:
            dependency_tree[block.id] = Node(block.id)
            if block.min_z == 1:
                continue
            found_obstacle = False
            while block.min_z > 1 and not found_obstacle:
                block.move_down()
                for obstacle in [
                    ob
                    for ob in obstacles
                    if ob.max_z == block.min_z and ob.id != block.id
                ]:
                    if obstacle.intersects(block):
                        found_obstacle = True
                        dependency_tree[obstacle.id].children.add(
                            dependency_tree[block.id]
                        )
                        dependency_tree[block.id].parents.add(
                            dependency_tree[obstacle.id]
                        )
                if found_obstacle:
                    block.move_up()
                    break
        total = 0
        for node in dependency_tree.values():
            total += node.destroy()
            for node in dependency_tree.values():
                node.destroyed = False
        return total


if __name__ == "__main__":
    Challenge22().run()
