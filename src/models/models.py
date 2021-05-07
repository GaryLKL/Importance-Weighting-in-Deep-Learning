import torch
import torch.nn as nn


# ResNet
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None, use_batchnorm=True):
        super(ResidualBlock, self).__init__()
        self.conv1 = conv3x3(in_channels, out_channels, stride)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(out_channels, out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample
        self.use_batchnorm = use_batchnorm
        
    def forward(self, x):
        residual = x
        
        if self.use_batchnorm:
            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu(out)
            out = self.conv2(out)
            out = self.bn2(out)
        else:
            out = self.conv1(x)
            out = self.relu(out)
            out = self.conv2(out)
            
        if self.downsample:
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out
    
    
class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=10, use_batchnorm=True):
        super(ResNet, self).__init__()
        self.in_channels = 64
        self.use_batchnorm = use_batchnorm
        self.conv = conv3x3(3, 64, kernel=5)
        self.bn = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.layer1 = self.make_layer(block, 64, layers[0])
        self.layer2 = self.make_layer(block, 128, layers[1], 2)
        self.layer3 = self.make_layer(block, 256, layers[2], 2)
        self.avg_pool = nn.AvgPool2d(8)
        self.fc = nn.Linear(256, num_classes)

    def make_layer(self, block, out_channels, blocks, stride=1):
        downsample = None
        if (stride != 1) or (self.in_channels != out_channels):
            if self.use_batchnorm:
                downsample = nn.Sequential(
                    conv3x3(self.in_channels, out_channels, stride=stride),
                    nn.BatchNorm2d(out_channels))
            else:
                conv3x3(self.in_channels, out_channels, stride=stride)
        layers = []
        layers.append(block(self.in_channels, out_channels, stride, downsample, use_batchnorm=self.use_batchnorm))
        self.in_channels = out_channels
        for i in range(1, blocks):
            layers.append(block(out_channels, out_channels, use_batchnorm=self.use_batchnorm))
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv(x)
        
        if self.use_batchnorm:
            out = self.bn(out)
            
        out = self.relu(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.avg_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

    
def conv3x3(in_channels, out_channels, stride=1, kernel=3):
    return nn.Conv2d(in_channels, out_channels, kernel_size=kernel, 
                     stride=stride, padding=1, bias=False)