# coding=utf-8
import os
import matplotlib.pyplot as plt

import conf

def img_show(img, text=None, save=False):
    npimg = img.numpy()
    plt.axis("off")
    if text:
        plt.text(75, 8, text, style='italic', fontweight='bold',
                 bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 10})
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

def show_plot(iteration, loss):
    plt.plot(iteration, loss)
    plt.show()

def convert(train=True):
    if(train):
        f = open(conf.txt_train_data, 'w')
        data_path = os.path.join(conf.root, 'att_faces/')
        print data_path
        if(not os.path.exists(data_path)):
            os.makedirs(data_path)
        for i in range(40):
            for j in range(10):
                img_path = data_path+'s'+str(i+1)+'/'+str(j+1)+'.pgm'
                print img_path
                f.write(img_path+' '+str(i)+'\n')
        f.close()


if __name__ == "__main__":
    convert()