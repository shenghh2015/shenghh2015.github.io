import numpy as np
import matplotlib.pyplot as plt
import os
from natsort import natsorted
from skimage import io

def norm2rgb(data):
		return np.uint8(255.* (data - data.min()) /(data.max() - data.min()))

def gray2rgb(image):
		zeros = np.zeros(image.shape, dtype = np.uint8)
		return np.stack([zeros, image, zeros], axis = -1)

def plot_pred(result_dir, img_idx, data_dic, colorbar = True, normalize = False, add_contrast = 100):
		from matplotlib.backends.backend_agg import FigureCanvasAgg
		from matplotlib.figure import Figure
		from skimage import io
		font_size = 28; label_size = 20
		rows, cols, size = 2,3,6
		size_shrink = 1
		widths = [size_shrink, 1, 1]; heights = [size_shrink, 1]; gs_kw = dict(width_ratios=widths, height_ratios=heights)
		fig = Figure(tight_layout=True,figsize=(size*cols, size*rows)); ax = fig.subplots(nrows=rows, ncols=cols, gridspec_kw=gs_kw)
		ph_img = data_dic['ph'][img_idx]
		gt = gray2rgb(data_dic['gt'][img_idx])
		pr_1i = gray2rgb(data_dic['pr_1i'][img_idx])
		d_1i = gray2rgb(data_dic['d_1i'][img_idx])
		pr_3i = gray2rgb(data_dic['pr_3i'][img_idx])
		d_3i = gray2rgb(data_dic['d_3i'][img_idx])
		if normalize:
				nm = True
				if nm:
						gt = norm2rgb(gt)
						pr_1i = norm2rgb(pr_1i)
						d_1i = norm2rgb(d_1i)
						pr_3i = norm3rgb(pr_3i)
						d_3i = norm2rgb(d_3i)
				#cmin, cmax = gt.min(), gt.max()
				cx0 = ax[0,0].imshow(ph_img); cx1 = ax[0,1].imshow(pr_1i, vmin = cmin, vmax = cmax)
				cx2 = ax[0,2].imshow(d_1i, vmin = cmin, vmax = cmax); cx3 = ax[1,0].imshow(gt, vmin = cmin, vmax = cmax)
				cx4 = ax[1,1].imshow(pr_3i, vmin = cmin, vmax = cmax); cx5 = ax[1,2].imshow(d_3i, vmin = cmin, vmax = cmax)
		else:	
				cx0 = ax[0,0].imshow(ph_img); cx1 = ax[0,1].imshow(pr_1i)
				cx2 = ax[0,2].imshow(d_1i); cx3 = ax[1,0].imshow(gt)
				cx4 = ax[1,1].imshow(pr_3i); cx5 = ax[1,2].imshow(d_3i)
		ax[0,0].set_xticks([]); ax[0,0].set_yticks([])
		ax[0,1].set_xticks([]); ax[0,2].set_xticks([])# ax[0,3].set_xticks([])
		ax[1,0].set_xticks([]); ax[1,1].set_xticks([]); ax[1,2].set_xticks([])# ax[1,3].set_xticks([])
		ax[0,1].set_yticks([]); ax[0,2].set_yticks([])# ax[0,3].set_yticks([])
		ax[1,1].set_yticks([]); ax[1,2].set_yticks([])# ax[1,3].set_yticks([])
		if colorbar:
			shrink_rate = 0.68
			cmin, cmax = 0, 255
			cbar = fig.colorbar(cx0, ax = ax[0,0], shrink = shrink_rate); cbar.ax.tick_params(labelsize=label_size)
			#cbar.set_clim(ph_img.min(), ph_img.max())
			cbar = fig.colorbar(cx1, ax = ax[0,1], shrink = shrink_rate); cbar.ax.tick_params(labelsize=label_size); #cbar.set_clim(cmin, cmax)
			cbar = fig.colorbar(cx2, ax = ax[0,2], shrink = shrink_rate); cbar.ax.tick_params(labelsize=label_size); #cbar.set_clim(cmin, cmax)
			cbar = fig.colorbar(cx3, ax = ax[1,0], shrink = shrink_rate); cbar.ax.tick_params(labelsize=label_size); #cbar.set_clim(cmin, cmax)
			cbar = fig.colorbar(cx4, ax = ax[1,1], shrink = shrink_rate); cbar.ax.tick_params(labelsize=label_size); #cbar.set_clim(cmin, cmax)
			cbar = fig.colorbar(cx5, ax = ax[1,2], shrink = shrink_rate); cbar.ax.tick_params(labelsize=label_size); #cbar.set_clim(cmin, cmax)
		ax[0,0].set_title('Image',fontsize=font_size);
		ax[0,1].set_title('Pr (1 plane)',fontsize=font_size);
		ax[0,2].set_title('Err map (1 plane)',fontsize=font_size);
		ax[1,0].set_title('GT',fontsize=font_size);
		ax[1,1].set_title('Pr (3 planes)',fontsize=font_size);
		ax[1,2].set_title('Err map (3 planes)',fontsize=font_size);
		fig.tight_layout(pad=-2)
		file_name = result_dir + '/z-{:03d}.png'.format(img_idx)
		canvas = FigureCanvasAgg(fig); canvas.print_figure(file_name, dpi=80)

# i = 150
# plot_pred(sample_dir, i, data_dict, colorbar = True)

def gen_folder(dir):
		if not os.path.exists(dir):
				os.system('mkdir -p {}'.format(dir))

def plot_pred_separately(result_dir, img_idx, data_dic, colorbar = True):
		from matplotlib.backends.backend_agg import FigureCanvasAgg
		from matplotlib.figure import Figure
		from skimage import io
		import random
		font_size = 28; label_size = 18
		# load data
		ph_img = data_dic['ph'][img_idx]
		gt = gray2rgb(data_dic['gt'][img_idx])
		pr_1i = gray2rgb(data_dic['pr_1i'][img_idx])
		d_1i = gray2rgb(data_dic['d_1i'][img_idx])
		pr_3i = gray2rgb(data_dic['pr_3i'][img_idx])
		d_3i = gray2rgb(data_dic['d_3i'][img_idx])
		imgs = [ph_img, gt, pr_1i, d_1i, pr_3i, d_3i]
		# plot figures
		slice_folder = os.path.join(result_dir, 'z-{:03d}'.format(img_idx)); gen_folder(slice_folder)
		size, cols, rows = 6, 1, 1
		figs = [Figure(tight_layout=True, figsize=(size-1.0, size-1.2))]
		for i in range(1, 6):
				figs.append(Figure(tight_layout=True, figsize=(size, size-1.2)))
		axes = []
		caxes = []
		for i, fig in enumerate(figs):
				axes.append(fig.subplots(nrows=rows, ncols=cols))
				caxes.append(axes[i].imshow(imgs[i]))
				axes[i].tick_params(axis = 'both', labelsize = label_size)
				if i > 0:
						#caxes.append(axes[i].imshow(imgs[i]))
						cbar = figs[i].colorbar(caxes[i], ax = axes[i], shrink = 0.93)
						cbar.ax.tick_params(labelsize=label_size)
		
		f_names = ['phase.png', 'gt_fl.png', 'pr_1i.png', 'd_1i.png', 'pr_3i.png', 'd_3i.png']
		for fig, fname in zip(figs, f_names):
				canvas = FigureCanvasAgg(fig)
				canvas.print_figure(slice_folder+'/{}'.format(fname), dpi=120)

def save_target_slices(result_dir, data_dic, slice_index):
		from skimage import io
		for name in data_dic:
			io.imsave(result_dir + '{}.tif'.format(name), data_dic[name][slice_index])

model_root = '/data/2d_models/neuron_float'

models = {'b0_1i':'Cor-FL1_FL2-net-Unet-bone-efficientnetb0-pre-True-epoch-400-batch-14-lr-0.0001-dim-512-train-None-rot-50.0-set-neuron_float-subset-train-loss-mse-act-relu-scale-100.0-decay-0.8-delta-10-chi-1-cho-1-chf-fl2-bselect-True',
					'b0_3i':'Cor-FL1_FL2-net-Unet-bone-efficientnetb0-pre-True-epoch-400-batch-14-lr-0.0001-dim-512-train-None-rot-50.0-set-neuron_float-subset-train-loss-mse-act-relu-scale-100.0-decay-0.8-delta-10-chi-3-cho-1-chf-fl2-bselect-True',
					'b1_1i':'Cor-FL1_FL2-net-Unet-bone-efficientnetb1-pre-True-epoch-400-batch-14-lr-0.0001-dim-512-train-None-rot-50.0-set-neuron_float-subset-train-loss-mse-act-relu-scale-100.0-decay-0.8-delta-10-chi-1-cho-1-chf-fl2-bselect-True',
					'b1_3i':'Cor-FL1_FL2-net-Unet-bone-efficientnetb1-pre-True-epoch-400-batch-14-lr-0.0001-dim-512-train-None-rot-50.0-set-neuron_float-subset-train-loss-mse-act-relu-scale-100.0-decay-0.8-delta-10-chi-3-cho-1-chf-fl2-bselect-True'}

arc = 'b0'

model_name1 = models['{}_1i'.format(arc)]
model_name2 = models['{}_3i'.format(arc)]

samples = [
'neuron_tau_map2_trial5_output',
'neuron_tau_map2_trial6_output',
'neuron_tau_map2_trial7_output',
'neuron_tau_map2_trial8_output',
'neuron_tau_map2_trial23_output',
'neuron_tau_map2_trial24_output',
'neuron_tau_map2_trial25_output',
'neuron_tau_map2_trial26_output']

# samples = [
# 'neuron_tau_map2_trial5_output',]

sample_name = 'neuron_tau_map2_trial6_output'

print(sample_name)
dataset_dir = '/data/datasets/'
pr1_file = model_root +'/' + model_name1 + '/pred_fl1_fl2_v1/Pr2_{}.npy'.format(sample_name)
pr2_file = model_root +'/' + model_name2 + '/pred_fl1_fl2_v1/Pr2_{}.npy'.format(sample_name)
gt_file = model_root +'/' + model_name1 + '/pred_fl1_fl2_v1/GT2_{}.npy'.format(sample_name)
ph_dir = '/data/datasets/neuron_float/data/{}/phase/'.format(sample_name)
pr1 = np.load(pr1_file)
pr2 = np.load(pr2_file)
gt = np.load(gt_file)
d1 = np.uint8(np.abs(pr1 - gt))
d2 = np.uint8(np.abs(pr2 - gt))
pr1 = norm2rgb(pr1)
pr2 = norm2rgb(pr2)
gt = np.uint8(gt)
ph_vol = np.stack([np.load(ph_dir + '/' + name)[:,:,1] for name in natsorted(os.listdir(ph_dir))])
data_dict = {'ph':ph_vol, 'gt': gt, 'pr_1i': pr1, 'pr_3i': pr2, 'd_1i':d1, 'd_3i': d2}

# save results
sample_dir = './grant_example/{}/'.format(sample_name)
gen_folder(sample_dir)
slice_index = 135
save_target_slices(sample_dir, data_dict, slice_index)
		
# 		for i in range(ph_vol.shape[0]):
# 			if i % 20 == 0: print('{}-th slice'.format(i))
# 			plot_pred(sample_dir, i, data_dict, colorbar = True, normalize = True)
		

for sample_name in samples:
		print(sample_name)
		dataset_dir = '/data/datasets/'
		pr1_file = model_root +'/' + model_name1 + '/pred_fl1_fl2_v1/Pr2_{}.npy'.format(sample_name)
		pr2_file = model_root +'/' + model_name2 + '/pred_fl1_fl2_v1/Pr2_{}.npy'.format(sample_name)
		gt_file = model_root +'/' + model_name1 + '/pred_fl1_fl2_v1/GT2_{}.npy'.format(sample_name)
		ph_dir = '/data/datasets/neuron_float/data/{}/phase/'.format(sample_name)
		pr1 = np.load(pr1_file)
		pr2 = np.load(pr2_file)
		gt = np.load(gt_file)
		d1 = np.uint8(np.abs(pr1 - gt))
		d2 = np.uint8(np.abs(pr2 - gt))
		pr1 = norm2rgb(pr1)
		pr2 = norm2rgb(pr2)
		gt = np.uint8(gt)
		ph_vol = np.stack([np.load(ph_dir + '/' + name)[:,:,1] for name in natsorted(os.listdir(ph_dir))])
		data_dict = {'ph':ph_vol, 'gt': gt, 'pr_1i': pr1, 'pr_3i': pr2, 'd_1i':d1, 'd_3i': d2}

		# save results
		sample_dir = './joint_fig_results/{}'.format(sample_name)
		gen_folder(sample_dir)
		index_set = [120, 160]
		#for i in range(ph_vol.shape[0]):
		for i in range(index_set):
			if i % 20 == 0: print('{}-th slice'.format(i))
			plot_pred(sample_dir, i, data_dict, colorbar = True, normalize = True)
		# save results
		
		# save results separately
		#sample_dir = './separate_fig_results/{}'.format(sample_name)
		#gen_folder(sample_dir)
		#for i in range(ph_vol.shape[0]):
		#		plot_pred_separately(sample_dir, i, data_dict, colorbar = True)
