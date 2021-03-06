import math
# TODO: Add some algorithm to have ridges


class FromCoast:

    def generate(self, map_obj):
        # FIXME: Lakes can be not just on 0 elevation, and rivers can flow from lake to ocean
        # By default elevation is 0. water corners have 0 elevation.
        corners_queue = []
        for corner in map_obj.corners:
            if corner.coast or (corner.water and not corner.ocean):
                corners_queue.append(corner)
            elif not corner.water:
                corner.elevation = None

        # increase elevation from coast to the center of island
        while corners_queue:
            corner = corners_queue.pop(0)
            for neigh in corner.adjacent:
                if neigh.elevation is None:
                    neigh.elevation = corner.elevation + 1
                    corners_queue.append(neigh)

        self._redistribute_elevations(map_obj.land_corners)

        # calculate elevation for centers
        for center in map_obj.centers:
            center.elevation = sum([c.elevation for c in center.corners]) / len(center.corners)

    def _redistribute_elevations(self, corners):
        """
        Change the overall distribution of elevations so that lower
        elevations are more common than higher
        elevations. Specifically, we want elevation X to have frequency
        (1-X).  To do this we will sort the corners, then set each
        corner to its desired elevation.

        Copied from https://github.com/amitp/mapgen2/blob/master/Map.as#L466
        """
        # SCALE_FACTOR increases the mountain area. At 1.0 the maximum
        # elevation barely shows up on the map, so you can set it to 1.1.
        SCALE_FACTOR = 1.1
        corners.sort(key=lambda c: c.elevation)

        for i, corner in enumerate(corners):
            # Let y(x) be the total area that we want at elevation <= x.
            # We want the higher elevations to occur less than lower
            # ones, and set the area to be y(x) = 1 - (1-x)^2.
            y = i / (len(corners) - 1)
            # Now we have to solve for x, given the known y.
            #   y = 1 - (1-x)^2
            #   y = 1 - (1 - 2x + x^2)
            #   y = 2x - x^2
            #   x^2 - 2x + y = 0
            # From this we can use the quadratic equation to get:
            corner.elevation = math.sqrt(SCALE_FACTOR) - math.sqrt(SCALE_FACTOR * (1 - y))
            if corner.elevation > 1:
                corner.elevation = 1.
