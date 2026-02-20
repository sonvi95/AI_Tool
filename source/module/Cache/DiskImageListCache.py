import os
import cv2

class DiskImageListCache:
    def __init__(self, root="image_cache", ext=".png"):
        self.root = root
        self.ext = ext
        os.makedirs(root, exist_ok=True)

    def key_dir(self, key):
        return os.path.join(self.root, key)

    def exists(self, key):
        d = self.key_dir(key)
        return os.path.isdir(d) and len(os.listdir(d)) > 0

    def save(self, key, images):
        """
        images: List[np.ndarray] (H,W,3) uint8
        """
        d = self.key_dir(key)
        os.makedirs(d, exist_ok=True)

        for i, img in enumerate(images):
            path = os.path.join(d, f"{i:03d}{self.ext}")
            cv2.imwrite(path, img)

    def load(self, key):
        d = self.key_dir(key)
        if not os.path.isdir(d):
            return None

        files = sorted(f for f in os.listdir(d) if f.endswith(self.ext))
        if not files:
            return None

        images = []
        for f in files:
            img = cv2.imread(os.path.join(d, f))
            if img is not None:
                images.append(img)
        return images

DISK = DiskImageListCache()