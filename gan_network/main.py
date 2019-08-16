# coding=utf-8

import argparse
import torch
import torchvision
import torchvision.utils
import torch.nn as nn
from random import randint

from model import NetD,NetG
import conf

transforms = torchvision.transforms.Compose([
    torchvision.transfroms.Scale(conf.image_size),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])

def train():
    dataset = torchvision.datasets.ImageFolder(conf.data_path, transform=transforms)   
    dataloader = torch.utils.data.DataLoader(
        dataset = dataset,
        batch_size = conf.batch_size,
        shuffle = True,
        drop_last = True
    )
    netG = NetG(conf.ngf, conf.nz)
    netD = NetD(conf.ndf)
    
    criterion = nn.BCELoss()
    optimizerG = torch.optim.Adam(netG.parameters(), lr=conf.lr, betas=(conf.beta1, 0.999))
    optimizerD = torch.optim.Adam(netD.parameters(), lr=conf.lr, betas=(conf.beta1, 0.999))

    label = torch.FloatTensor(conf.batch_size)
    real_label = 1
    fake_label = 0

    for epoch in range(1, conf.epoch+1):
        for i,(imgs,_) in enumerate(dataloader):
            optimizerD.zero_grad()
            output = netD(imgs)
            label.data.fill_(real_label)
            errD_real = criterion(output, label)
            errD_real.backward()
            label.data.fill_(fake_label)
            noise = torch.randn(conf.batch_size, conf.nz, 1, 1)
            fake = netG(noise) #生成假图
            output = netD(fake.detach())
            errD_fake = criterion(output, label)
            errD_fake.backward()
            errD = errD_fake + errD_real
            optimizerD.step()

            optimizerD.zero_grad()
            label.data.fill_(real_label)
            output = netD(fake)
            errG = criterion(output, label)
            errG.backward()
            optimizerG.step()
        #end-for
        torch.utils.save_image(fake.data)
        torch.save(negG.state_dict())
        torch.save(negD.state_dict())

def main():
    train()
    #test()

if __name__ == "__main__":
    main()