from shared import BaseChallenge
import numpy as np
from scipy.spatial.distance import pdist


def dist_ind_to_pair_ind(d: int, i: int) -> tuple[int, int]:
    b = 1 - 2 * d
    x = np.floor((-b - np.sqrt(b**2 - 8 * i)) / 2).astype(int)
    y = (i + x * (b + x + 2) / 2 + 1).astype(int)
    return (x, y)


class Challenge8(BaseChallenge):
    def first(self, num_connections: int = 1000) -> int:
        total = 1
        lines = tuple(self.stripped_lines)
        points = np.empty((len(lines), 3), dtype=int)
        connections: list[set[int]] = []
        for i, line in enumerate(lines):
            x, y, z = map(int, line.split(","))
            points[i] = np.array([x, y, z])
        dists = pdist(points)
        sorted_dists = dists.argsort()
        for dist in sorted_dists[:num_connections]:
            a, b = dist_ind_to_pair_ind(len(lines), dist)
            left_set = None
            for conn in connections.copy():
                if a in conn or b in conn:
                    if left_set is not None:
                        left_set.update(conn)
                        connections.remove(conn)
                        break
                    conn.add(a)
                    conn.add(b)
                    left_set = conn
            if left_set is None:
                connections.append({a, b})
        sorted_connections = sorted(connections, key=lambda x: -len(x))
        for i in range(min(3, len(sorted_connections))):
            total *= len(sorted_connections[i])
        return total

    def second(self) -> int:
        total = 1
        lines = tuple(self.stripped_lines)
        points = np.empty((len(lines), 3), dtype=int)
        connections: list[set[int]] = []
        for i, line in enumerate(lines):
            x, y, z = map(int, line.split(","))
            points[i] = np.array([x, y, z])
        dists = pdist(points)
        sorted_dists = dists.argsort()
        a, b = -1, -1
        for dist in sorted_dists:
            a, b = dist_ind_to_pair_ind(len(lines), dist)
            left_set = None
            for conn in connections.copy():
                if a in conn or b in conn:
                    if left_set is not None:
                        left_set.update(conn)
                        connections.remove(conn)
                        break
                    conn.add(a)
                    conn.add(b)
                    left_set = conn
            if left_set is None:
                connections.append({a, b})
            if len(connections) == 1 and len(connections[0]) == len(lines):
                break
        return points[a][0] * points[b][0]


if __name__ == "__main__":
    Challenge8().run()
