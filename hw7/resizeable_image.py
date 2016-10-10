import sys
import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        w = self.width
        h = self.height
        energy = [[self.energy(i, j) for j in range(h)] for i in range(w)]
        dp = {}
        for i in xrange(w):
            dp[(i,0)] = energy[i][0]

        backpointer = {}
        for j in range(1, h):
            for i in range(w):
                backpointer[i,j] = 0
                dp[i,j] = dp[i,j-1]+energy[i][j]
                if i != 0 and dp[i,j] > dp[i-1,j-1]+energy[i][j]:
                    dp[i,j]=dp[i-1,j-1]+energy[i][j]
                    backpointer[i,j]=-1
                if i != w-1 and dp[i,j]> dp[i+1,j-1]+energy[i][j]:
                    dp[i,j]=dp[i+1,j-1]+energy[i][j]
                    backpointer[i,j]=1
        bestv = sys.maxint
        index = None
        for i in range(w):
            if dp[i,h-1] < bestv:
                bestv = dp[i,h-1]
                index = i

        seam = []
        for j in range(h-1, 0, -1):
            seam.append((index,j))
            index = index + backpointer[index,j]
        seam.append((index,0))
        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
