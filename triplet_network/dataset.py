
from PIL import Image
import os
import os.path

def default_image_loader(path):
    return Image.open(path).convert("RGB")

class TripletImageLoader(torch.utils.data.Dataset):
    def __init__(self, base_path, filenames_filename, triplets_file_name, transform=None,
                 loader=default_image_loader):
        self.base_path = base_path
        self.file_name_list = []
        for line in open(filenames_filename):
            self.file_name_list.append(line.rstrip("\n"))
        triplets = []
        for line in open(triplets_file_name):
            triplets.append((line.split()[0], line.split()[1], line.split()[2])) #anchor, far, close
        self.triplets = triplets
        self.transform = transform
        self.loader = loader
    
    def __getitem__(self, index):
        path1, path2, path3 = self.triplets[index]
        img1 = self.loader(os.path.join(self.base_path, self.file_name_list[int(path1)]))
        img2 = self.loader(os.path.join(self.base_path, self.file_name_list[int(path2)]))
        img3 = self.loader(os.path.join(self.base_path, self.file_name_list[int(path3)]))
        if self.transform is not None:
            img1 = self.transform(img1)
            img2 = self.transform(img2)
            img3 = self.transform(img3)
        return img1,img2,img3
        
    def __len__(self):
        return len(self.triplets)

