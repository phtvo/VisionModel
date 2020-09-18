import sys 
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../', '..'))

from Backbone.Hourglass import hourglass as hg 
import torch

from time import time

channels = 192

def test_module(channels):

    hg.use_bb_with_dw = True
    hg_module = hg.hourglass_module(input_size=channels, 
                                    basic_block_callback= hg.basic_block)
    hg_module.eval()

    #print(hg_module)

    x = torch.ones((1, channels, 64, 64))

    ## timing cpu
    for _ in range(5):
        with torch.no_grad():
            tic = time()
            hg_module(x)
            print(f'time: {round(time() - tic, 4)*1000} ms')
    ## timing gpu
    hg_module.cuda()
    x = x.type(torch.cuda.FloatTensor).cuda()
    for _ in range(5):
        with torch.no_grad():
            tic = time()
            hg_module(x)
            print(f'time: {round(time() - tic, 4)*1000} ms')

    hg_module.cpu()
    # number of paramters
    s = 0
    for m in hg_module.parameters():
        s += m.cpu().numel()
    print(s)

#####

def test_model():
    x = torch.ones((1, 3, 256, 256))
    hg.use_bb_with_dw = False
    
    hg_model = hg.hourglass(n_heatmaps= 19, stacked_ch= 128)
    #hg_model = torch.nn.DataParallel(hg_model)
    
    hg_model.eval()

    ## timing cpu
    for _ in range(5):
        with torch.no_grad():
            tic = time()
            hg_model(x)
            print(f'time: {round(time() - tic, 4)*1000} ms')
    ## timing gpu
    hg_model.cuda()
    x = x.type(torch.cuda.FloatTensor).cuda()
    for _ in range(5):
        with torch.no_grad():
            tic = time()
            hg_model(x, True)
            print(f'time: {round(time() - tic, 4)*1000} ms')

    hg_model.cpu()
    # number of paramters
    s = 0
    for m in hg_model.parameters():
        s += m.cpu().numel()
    print(s)
    
    return hg_model 
    
model = test_model()
#torch.save(model.state_dict(), 'hg.pth')