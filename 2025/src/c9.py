from shared import BaseChallenge
import numpy as np
from scipy.spatial.distance import pdist

# from matplotlib import pyplot as plt


class Challenge9(BaseChallenge):
    def first(self) -> int:
        lines = tuple(self.stripped_lines)
        points = np.empty((len(lines), 2), dtype=int)
        for i, line in enumerate(lines):
            x, y = map(int, line.split(","))
            points[i] = np.array([x, y])
        dists = pdist(points, lambda u, v: abs(u[0] - v[0] + 1) * abs(u[1] - v[1] + 1))
        sorted_dists = reversed(dists.argsort())
        return dists[next(sorted_dists)].astype(int)

    def dist_ind_to_pair_ind(self, d: int, i: int) -> tuple[int, int]:
        b = 1 - 2 * d
        x = (-b - np.sqrt(b**2 - 8 * i)) // 2
        y = i + x * (b + x + 2) / 2 + 1
        return (int(x), int(y))

    def draw_line(self, space: np.ndarray, p1: np.ndarray, p2: np.ndarray):
        x_min = min(p1[0], p2[0])
        x_max = max(p1[0], p2[0])
        y_min = min(p1[1], p2[1])
        y_max = max(p1[1], p2[1])
        space[x_min : x_max + 1, y_min : y_max + 1] = 1

    def get_compressed_matrix(self, points: np.ndarray) -> tuple[np.ndarray, dict[tuple[int, int], tuple[int, int]]]:
        points_x_sorted = sorted(set(points[:, 0]))
        points_y_sorted = sorted(set(points[:, 1]))
        points_x_dict = {x: i for i, x in enumerate(points_x_sorted)}
        points_y_dict = {y: i for i, y in enumerate(points_y_sorted)}

        matrix = np.zeros((len(points_x_sorted), len(points_y_sorted)), dtype=np.int8)
        point_to_compressed_coords = {}
        for point in points:
            point_to_compressed_coords[tuple(point)] = (points_x_dict[point[0]], points_y_dict[point[1]])
            matrix[points_x_dict[point[0]], points_y_dict[point[1]]] = 1
        return matrix, point_to_compressed_coords

    def second(self) -> int:
        lines = tuple(self.stripped_lines)
        points = np.empty((len(lines), 2), dtype=int)
        for i, line in enumerate(lines):
            x, y = map(int, line.split(","))
            points[i] = np.array([x, y])

        space, point_to_compressed_coords = self.get_compressed_matrix(points)

        for i, point in enumerate(points[:-1]):
            next_point = points[i + 1]
            self.draw_line(
                space, point_to_compressed_coords[tuple(point)], point_to_compressed_coords[tuple(next_point)]
            )
        self.draw_line(
            space, point_to_compressed_coords[tuple(points[-1])], point_to_compressed_coords[tuple(points[0])]
        )
        # plt.matshow(space.T)
        # plt.show()

        dists = pdist(points, lambda u, v: (abs(u[0] - v[0]) + 1) * (abs(u[1] - v[1]) + 1))
        sorted_dists = reversed(dists.argsort())
        for dist in sorted_dists:
            p1, p2 = self.dist_ind_to_pair_ind(len(points), dist)
            compressed_p1 = point_to_compressed_coords[tuple(points[p1])]
            compressed_p2 = point_to_compressed_coords[tuple(points[p2])]
            min_x = min(compressed_p1[0], compressed_p2[0])
            max_x = max(compressed_p1[0], compressed_p2[0])
            min_y = min(compressed_p1[1], compressed_p2[1])
            max_y = max(compressed_p1[1], compressed_p2[1])
            if (
                any(space[min_x, 0 : min_y + 1] != 0)
                and any(space[min_x, max_y : space.shape[1]] != 0)
                and any(space[max_x, 0 : min_y + 1] != 0)
                and any(space[max_x, max_y : space.shape[1]] != 0)
                and all(space[min_x + 1 : max_x, min_y + 1 : max_y].flatten() == 0)
            ):
                temp_space = space.copy()
                temp_space[compressed_p1[0], compressed_p1[1]] = 3
                temp_space[compressed_p2[0], compressed_p2[1]] = 3
                # plt.matshow(temp_space.T)
                # plt.show()
                return dists[dist].astype(int)

        raise ValueError("No valid pair found")


if __name__ == "__main__":
    Challenge9().run()
