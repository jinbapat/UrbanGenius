# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17mlzSPNNbkB1Y92b5MtK4AXbjkI00dpi
"""

import tensorflow as tf

import os
import pathlib
import time
import datetime

from matplotlib import pyplot as plt
from IPython import display

from google.colab import drive
drive.mount('/content/drive')

import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt

# Define the source and target folder paths
source_folder_path = '/content/drive/MyDrive/without_buildings'
target_folder_path = '/content/drive/MyDrive/processed_images'

# Create the target folder if it doesn't exist
os.makedirs(target_folder_path, exist_ok=True)

# Get a list of all PNG files in the source folder
image_files = [os.path.join(source_folder_path, f) for f in os.listdir(source_folder_path) if f.endswith('.png')]

# Check if there are any image files
if not image_files:
    print("No image files found in the folder.")
else:
    # Loop through each file and process it
    for image_file in image_files:
        print(f"Processing image: {image_file}")

        # Read and decode the image using TensorFlow
        sample_image = tf.io.read_file(image_file)
        sample_image = tf.io.decode_png(sample_image)
        print(f"TensorFlow image shape for {image_file}: {sample_image.shape}")

        # Open and process the image using PIL
        image = Image.open(image_file)
        width, height = image.size
        print(f"PIL image size for {image_file}: {width}x{height}")

        # Display the image using matplotlib
        plt.figure()
        plt.imshow(image, cmap="Greys")
        plt.title(f"Image: {image_file}")
        plt.show()

        # Limit the number of pixel values printed
        max_pixels_to_print = 220
        pixel_count = 0

        # Loop through each pixel and print its value
        for y in range(height):
            for x in range(width):
                if pixel_count >= max_pixels_to_print:
                    break
                pixel_value = image.getpixel((x, y))
                print(f'Pixel value at ({x}, {y}) in {image_file}: {pixel_value}')
                pixel_count += 1
            if pixel_count >= max_pixels_to_print:
                break

        # Save the processed image to the target folder
        processed_image_path = os.path.join(target_folder_path, os.path.basename(image_file))
        image.save(processed_image_path)
        print(f"Processed image saved to: {processed_image_path}")

import os
import tensorflow as tf
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

# Define the source and target folder paths
source_folder_path = '/content/drive/MyDrive/grayscale_with_buildings'
target_folder_path = '/content/drive/MyDrive/processed_images_2'

# Create the target folder if it doesn't exist
os.makedirs(target_folder_path, exist_ok=True)

# Get a list of all PNG files in the source folder
image_files = [os.path.join(source_folder_path, f) for f in os.listdir(source_folder_path) if f.endswith('.png')]

# Check if there are any image files
if not image_files:
    print("No image files found in the folder.")
else:
    # Loop through each file and process it
    for image_file in image_files:
        print(f"Processing image: {image_file}")

        # Read and decode the image using TensorFlow
        sample_image = tf.io.read_file(image_file)
        sample_image = tf.io.decode_png(sample_image)
        print(f"TensorFlow image shape for {image_file}: {sample_image.shape}")

        # Open and process the image using PIL
        image = Image.open(image_file)
        width, height = image.size
        print(f"PIL image size for {image_file}: {width}x{height}")

        # Increase the contrast of the image
        contrast_enhancer = ImageEnhance.Contrast(image)
        image_contrast_enhanced = contrast_enhancer.enhance(2.0)  # Increase the contrast by a factor of 2.0

        # Increase the brightness of the image
        brightness_enhancer = ImageEnhance.Brightness(image_contrast_enhanced)
        image_enhanced = brightness_enhancer.enhance(1.5)  # Increase the brightness by a factor of 1.5

        # Display the enhanced image using matplotlib with different shades of grey
        plt.figure()
        plt.imshow(image_enhanced, cmap="gray")
        plt.title(f"Image: {image_file}")

        # Save the enhanced image with the different shades of grey
        processed_image_path = os.path.join(target_folder_path, os.path.basename(image_file))
        plt.savefig(processed_image_path)

        # Show the plot
        plt.show()

        # Close the plot
        plt.close()
        print(f"Processed image saved to: {processed_image_path}")

        # Limit the number of pixel values printed
        max_pixels_to_print = 220
        pixel_count = 0

        # Loop through each pixel and print its value
        for y in range(height):
            for x in range(width):
                if pixel_count >= max_pixels_to_print:
                    break
                pixel_value = image.getpixel((x, y))
                print(f'Pixel value at ({x, y}) in {image_file}: {pixel_value}')
                pixel_count += 1
            if pixel_count >= max_pixels_to_print:
                break

# The facade training set consist of 400 images
BUFFER_SIZE = 200
# The batch size of 1 produced better results for the U-Net in the original pix2pix experiment
BATCH_SIZE = 1
# Each image is 256x256 in size
IMG_WIDTH = 256
IMG_HEIGHT = 256

# Define the resize function
def resize(input_image, real_image, height, width):
    input_image = tf.image.resize(input_image, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    real_image = tf.image.resize(real_image, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    return input_image, real_image

def random_crop(input_image, real_image):
    stacked_image = tf.stack([input_image, real_image], axis=0)
    cropped_image = tf.image.random_crop(stacked_image, size=[2, 256, 256, 3])
    return cropped_image[0], cropped_image[1]

def normalize(input_image, real_image):
    input_image = (input_image / 127.5) - 1
    real_image = (real_image / 127.5) - 1
    return input_image, real_image

@tf.function
def random_jitter(input_image, real_image):
    # Resizing to 286x286
    input_image, real_image = resize(input_image, real_image, 286, 286)

    # Random cropping back to 256x256
    input_image, real_image = random_crop(input_image, real_image)

    if tf.random.uniform(()) > 0.5:
        # Random mirroring
        input_image = tf.image.flip_left_right(input_image)
        real_image = tf.image.flip_left_right(real_image)

    return input_image, real_image

import os
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf


# Define the source folder paths
source_folder_path1 = '/content/drive/MyDrive/without_buildings'  # Update with the actual path
source_folder_path2 = '/content/drive/MyDrive/grayscale_with_buildings'  # Update with the actual path

# Get the list of image files in the first folder
image_files1 = [f for f in os.listdir(source_folder_path1) if f.endswith('.png')]

# Check if there are matching images in the second folder
matching_files = [f for f in image_files1 if os.path.exists(os.path.join(source_folder_path2, f))]

# Ensure there are matching images in both folders
if not matching_files:
    print("No matching image files found in both folders.")
else:
    # Select an image with the same name from both folders
    for matching_file in matching_files:
        inp_path = os.path.join(source_folder_path1, matching_file)
        re_path = os.path.join(source_folder_path2, matching_file)

        inp = Image.open(inp_path)
        re = Image.open(re_path)

        # Convert images to tensors and ensure they have 3 dimensions (H, W, C)
        inp = tf.convert_to_tensor(inp, dtype=tf.float32)
        re = tf.convert_to_tensor(re, dtype=tf.float32)

        if inp.ndim == 2:  # If the image is grayscale, add a channel dimension
            inp = tf.expand_dims(inp, axis=-1)
        if re.ndim == 2:  # If the image is grayscale, add a channel dimension
            re = tf.expand_dims(re, axis=-1)

        inp = tf.image.grayscale_to_rgb(inp)  # Convert to 3 channels if needed
        re = tf.image.grayscale_to_rgb(re)    # Convert to 3 channels if needed

        plt.figure(figsize=(6, 6))

        for i in range(4):
            rj_inp, rj_re = random_jitter(inp, re)
            plt.subplot(2, 2, i + 1)
            plt.imshow(rj_inp / 255.0)
            plt.axis('off')

        plt.show()

def load_image_train(image_file):
    input_image, real_image = load(image_file)
    input_image, real_image = random_jitter(input_image, real_image)
    input_image, real_image = normalize(input_image, real_image)
    return input_image, real_image

def load_image_test(image_file):
    input_image, real_image = load(image_file)
    input_image, real_image = resize(input_image, real_image, 256, 256)
    input_image, real_image = normalize(input_image, real_image)
    return input_image, real_image

"""## Build an input pipeline with `tf.data`"""

train_dataset = tf.data.Dataset.list_files(str('/content/drive/MyDrive/grayscale_with_buildings/*'))
train_dataset = train_dataset.map(load_image_train, num_parallel_calls=tf.data.AUTOTUNE)
train_dataset = train_dataset.shuffle(BUFFER_SIZE)
train_dataset = train_dataset.batch(BATCH_SIZE)

OUTPUT_CHANNELS = 3

def downsample(filters, size, apply_batchnorm=True):
  initializer = tf.random_normal_initializer(0., 0.02)

  result = tf.keras.Sequential()
  result.add(
      tf.keras.layers.Conv2D(filters, size, strides=2, padding='same',
                             kernel_initializer=initializer, use_bias=False))

  if apply_batchnorm:
    result.add(tf.keras.layers.BatchNormalization())

  result.add(tf.keras.layers.LeakyReLU())

  return result

down_model = downsample(3, 4)
down_result = down_model(tf.expand_dims(inp, 0))
print (down_result.shape)

def upsample(filters, size, apply_dropout=False):
  initializer = tf.random_normal_initializer(0., 0.02)

  result = tf.keras.Sequential()
  result.add(
    tf.keras.layers.Conv2DTranspose(filters, size, strides=2,
                                    padding='same',
                                    kernel_initializer=initializer,
                                    use_bias=False))

  result.add(tf.keras.layers.BatchNormalization())

  if apply_dropout:
      result.add(tf.keras.layers.Dropout(0.5))

  result.add(tf.keras.layers.ReLU())

  return result

up_model = upsample(3, 4)
up_result = up_model(down_result)
print (up_result.shape)

def Generator():
  inputs = tf.keras.layers.Input(shape=[256, 256, 3])

  down_stack = [
    downsample(64, 4, apply_batchnorm=False),  # (batch_size, 128, 128, 64)
    downsample(128, 4),  # (batch_size, 64, 64, 128)
    downsample(256, 4),  # (batch_size, 32, 32, 256)
    downsample(512, 4),  # (batch_size, 16, 16, 512)
    downsample(512, 4),  # (batch_size, 8, 8, 512)
    downsample(512, 4),  # (batch_size, 4, 4, 512)
    downsample(512, 4),  # (batch_size, 2, 2, 512)
    downsample(512, 4),  # (batch_size, 1, 1, 512)
  ]

  up_stack = [
    upsample(512, 4, apply_dropout=True),  # (batch_size, 2, 2, 1024)
    upsample(512, 4, apply_dropout=True),  # (batch_size, 4, 4, 1024)
    upsample(512, 4, apply_dropout=True),  # (batch_size, 8, 8, 1024)
    upsample(512, 4),  # (batch_size, 16, 16, 1024)
    upsample(256, 4),  # (batch_size, 32, 32, 512)
    upsample(128, 4),  # (batch_size, 64, 64, 256)
    upsample(64, 4),  # (batch_size, 128, 128, 128)
  ]

  initializer = tf.random_normal_initializer(0., 0.02)
  last = tf.keras.layers.Conv2DTranspose(OUTPUT_CHANNELS, 4,
                                         strides=2,
                                         padding='same',
                                         kernel_initializer=initializer,
                                         activation='tanh')  # (batch_size, 256, 256, 3)

  x = inputs

  # Downsampling through the model
  skips = []
  for down in down_stack:
    x = down(x)
    skips.append(x)

  skips = reversed(skips[:-1])

  # Upsampling and establishing the skip connections
  for up, skip in zip(up_stack, skips):
    x = up(x)
    x = tf.keras.layers.Concatenate()([x, skip])

  x = last(x)

  return tf.keras.Model(inputs=inputs, outputs=x)

generator = Generator()
tf.keras.utils.plot_model(generator, show_shapes=True, dpi=64)

LAMBDA = 100

loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def generator_loss(disc_generated_output, gen_output, target):
  gan_loss = loss_object(tf.ones_like(disc_generated_output), disc_generated_output)

  # Mean absolute error
  l1_loss = tf.reduce_mean(tf.abs(target - gen_output))

  total_gen_loss = gan_loss + (LAMBDA * l1_loss)

  return total_gen_loss, gan_loss, l1_loss

def Discriminator():
  initializer = tf.random_normal_initializer(0., 0.02)

  inp = tf.keras.layers.Input(shape=[256, 256, 3], name='input_image')
  tar = tf.keras.layers.Input(shape=[256, 256, 3], name='target_image')

  x = tf.keras.layers.concatenate([inp, tar])  # (batch_size, 256, 256, channels*2)

  down1 = downsample(64, 4, False)(x)  # (batch_size, 128, 128, 64)
  down2 = downsample(128, 4)(down1)  # (batch_size, 64, 64, 128)
  down3 = downsample(256, 4)(down2)  # (batch_size, 32, 32, 256)

  zero_pad1 = tf.keras.layers.ZeroPadding2D()(down3)  # (batch_size, 34, 34, 256)
  conv = tf.keras.layers.Conv2D(512, 4, strides=1,
                                kernel_initializer=initializer,
                                use_bias=False)(zero_pad1)  # (batch_size, 31, 31, 512)

  batchnorm1 = tf.keras.layers.BatchNormalization()(conv)

  leaky_relu = tf.keras.layers.LeakyReLU()(batchnorm1)

  zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu)  # (batch_size, 33, 33, 512)

  last = tf.keras.layers.Conv2D(1, 4, strides=1,
                                kernel_initializer=initializer)(zero_pad2)  # (batch_size, 30, 30, 1)

  return tf.keras.Model(inputs=[inp, tar], outputs=last)

discriminator = Discriminator()
tf.keras.utils.plot_model(discriminator, show_shapes=True, dpi=64)

def discriminator_loss(disc_real_output, disc_generated_output):
  real_loss = loss_object(tf.ones_like(disc_real_output), disc_real_output)

  generated_loss = loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)

  total_disc_loss = real_loss + generated_loss

  return total_disc_loss

generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                 discriminator_optimizer=discriminator_optimizer,
                                 generator=generator,
                                 discriminator=discriminator)

def generate_images(model, test_input, tar):
  prediction = model(test_input, training=True)
  plt.figure(figsize=(15, 15))

  display_list = [test_input[0], tar[0], prediction[0]]
  title = ['Input Image', 'Ground Truth', 'Predicted Image']

  for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.title(title[i])
    # Getting the pixel values in the [0, 1] range to plot.
    plt.imshow(display_list[i] * 0.5 + 0.5)
    plt.axis('off')
  plt.show()

log_dir="logs/"

summary_writer = tf.summary.create_file_writer(
  log_dir + "fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

@tf.function
def train_step(input_image, target, step):
  with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
    gen_output = generator(input_image, training=True)

    disc_real_output = discriminator([input_image, target], training=True)
    disc_generated_output = discriminator([input_image, gen_output], training=True)

    gen_total_loss, gen_gan_loss, gen_l1_loss = generator_loss(disc_generated_output, gen_output, target)
    disc_loss = discriminator_loss(disc_real_output, disc_generated_output)

  generator_gradients = gen_tape.gradient(gen_total_loss,
                                          generator.trainable_variables)
  discriminator_gradients = disc_tape.gradient(disc_loss,
                                               discriminator.trainable_variables)

  generator_optimizer.apply_gradients(zip(generator_gradients,
                                          generator.trainable_variables))
  discriminator_optimizer.apply_gradients(zip(discriminator_gradients,
                                              discriminator.trainable_variables))

  with summary_writer.as_default():
    tf.summary.scalar('gen_total_loss', gen_total_loss, step=step//1000)
    tf.summary.scalar('gen_gan_loss', gen_gan_loss, step=step//1000)
    tf.summary.scalar('gen_l1_loss', gen_l1_loss, step=step//1000)
    tf.summary.scalar('disc_loss', disc_loss, step=step//1000)

def fit(train_ds, test_ds, steps):
  example_input, example_target = next(iter(test_ds.take(1)))
  start = time.time()

  for step, (input_image, target) in train_ds.repeat().take(steps).enumerate():
    if (step) % 1000 == 0:
      display.clear_output(wait=True)

      if step != 0:
        print(f'Time taken for 1000 steps: {time.time()-start:.2f} sec\n')

      start = time.time()

      generate_images(generator, example_input, example_target)
      print(f"Step: {step//1000}k")

    train_step(input_image, target, step)

    # Training step
    if (step+1) % 10 == 0:
      print('.', end='', flush=True)


    # Save (checkpoint) the model every 5k steps
    if (step + 1) % 5000 == 0:
      checkpoint.save(file_prefix=checkpoint_prefix)

# Restoring the latest checkpoint in checkpoint_dir
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))

"""SUGAN"""

def D_unet_arch(ch=64, attention='64',ksize='333333', dilation='111111',out_channel_multiplier=1):
    arch = {}

    n = 2

    ocm = out_channel_multiplier

    # covers bigger perceptual fields
    arch[128]= {'in_channels' :       [3] + [ch*item for item in       [1, 2, 4, 8, 16, 8*n, 4*2, 2*2, 1*2,1]],
                             'out_channels' : [item * ch for item in [1, 2, 4, 8, 16, 8,   4,   2,    1,  1]],
                             'downsample' : [True]*5 + [False]*5,
                             'upsample':    [False]*5+ [True] *5,
                             'resolution' : [64, 32, 16, 8, 4, 8, 16, 32, 64, 128],
                             'attention' : {2**i: 2**i in [int(item) for item in attention.split('_')]
                                                            for i in range(2,11)}}


    arch[256] = {'in_channels' :            [3] + [ch*item for item in [1, 2, 4, 8, 8, 16, 8*2, 8*2, 4*2, 2*2, 1*2  , 1         ]],
                             'out_channels' : [item * ch for item in [1, 2, 4, 8, 8, 16, 8,   8,   4,   2,   1,   1          ]],
                             'downsample' : [True] *6 + [False]*6 ,
                             'upsample':    [False]*6 + [True] *6,
                             'resolution' : [128, 64, 32, 16, 8, 4, 8, 16, 32, 64, 128, 256 ],
                             'attention' : {2**i: 2**i in [int(item) for item in attention.split('_')]
                                                            for i in range(2,13)}}



    return arch

import torch
import torch.nn as nn
class Unet_Discriminator(nn.Module):

    def __init__(self, D_ch=64, D_wide=True, resolution=128,
                             D_kernel_size=3, D_attn='64', n_classes=1000,
                             num_D_SVs=1, num_D_SV_itrs=1, D_activation=nn.ReLU(inplace=False),
                             D_lr=2e-4, D_B1=0.0, D_B2=0.999, adam_eps=1e-8,
                             SN_eps=1e-12, output_dim=1, D_mixed_precision=False, D_fp16=False,
                             D_init='ortho', skip_init=False, D_param='SN', decoder_skip_connection = True, **kwargs):
        super(Unet_Discriminator, self).__init__()


        # Width multiplier
        self.ch = D_ch
        # Use Wide D as in BigGAN and SA-GAN or skinny D as in SN-GAN?
        self.D_wide = D_wide
        # Resolution
        self.resolution = resolution
        # Kernel size
        self.kernel_size = D_kernel_size
        # Attention?
        self.attention = D_attn
        # Number of classes
        self.n_classes = n_classes
        # Activation
        self.activation = D_activation
        # Initialization style
        self.init = D_init
        # Parameterization style
        self.D_param = D_param
        # Epsilon for Spectral Norm?
        self.SN_eps = SN_eps
        # Fp16?
        self.fp16 = D_fp16



        if self.resolution==128:
            self.save_features = [0,1,2,3,4]
        elif self.resolution==256:
            self.save_features = [0,1,2,3,4,5]

        self.out_channel_multiplier = 1#4
        # Architecture
        self.arch = D_unet_arch(self.ch, self.attention , out_channel_multiplier = self.out_channel_multiplier  )[resolution]

        self.unconditional = kwargs["unconditional"]

        # Which convs, batchnorms, and linear layers to use
        # No option to turn off SN in D right now
        if self.D_param == 'SN':
            self.which_conv = functools.partial(layers.SNConv2d,
                                                    kernel_size=3, padding=1,
                                                    num_svs=num_D_SVs, num_itrs=num_D_SV_itrs,
                                                    eps=self.SN_eps)
            self.which_linear = functools.partial(layers.SNLinear,
                                                    num_svs=num_D_SVs, num_itrs=num_D_SV_itrs,
                                                    eps=self.SN_eps)

            self.which_embedding = functools.partial(layers.SNEmbedding,
                                                            num_svs=num_D_SVs, num_itrs=num_D_SV_itrs,
                                                            eps=self.SN_eps)
        # Prepare model
        # self.blocks is a doubly-nested list of modules, the outer loop intended
        # to be over blocks at a given resolution (resblocks and/or self-attention)
        self.blocks = []

        for index in range(len(self.arch['out_channels'])):

            if self.arch["downsample"][index]:
                self.blocks += [[layers.DBlock(in_channels=self.arch['in_channels'][index],
                                             out_channels=self.arch['out_channels'][index],
                                             which_conv=self.which_conv,
                                             wide=self.D_wide,
                                             activation=self.activation,
                                             preactivation=(index > 0),
                                             downsample=(nn.AvgPool2d(2) if self.arch['downsample'][index] else None))]]

            elif self.arch["upsample"][index]:
                upsample_function = (functools.partial(F.interpolate, scale_factor=2, mode="nearest") #mode=nearest is default
                                    if self.arch['upsample'][index] else None)

                self.blocks += [[layers.GBlock2(in_channels=self.arch['in_channels'][index],
                                                         out_channels=self.arch['out_channels'][index],
                                                         which_conv=self.which_conv,
                                                         #which_bn=self.which_bn,
                                                         activation=self.activation,
                                                         upsample= upsample_function, skip_connection = True )]]

            # If attention on this block, attach it to the end
            attention_condition = index < 5
            if self.arch['attention'][self.arch['resolution'][index]] and attention_condition: #index < 5
                print('Adding attention layer in D at resolution %d' % self.arch['resolution'][index])
                print("index = ", index)
                self.blocks[-1] += [layers.Attention(self.arch['out_channels'][index],
                                                                                         self.which_conv)]


        # Turn self.blocks into a ModuleList so that it's all properly registered.
        self.blocks = nn.ModuleList([nn.ModuleList(block) for block in self.blocks])


        last_layer = nn.Conv2d(self.ch*self.out_channel_multiplier,1,kernel_size=1)
        self.blocks.append(last_layer)
        #
        # Linear output layer. The output dimension is typically 1, but may be
        # larger if we're e.g. turning this into a VAE with an inference output
        self.linear = self.which_linear(self.arch['out_channels'][-1], output_dim)

        self.linear_middle = self.which_linear(16*self.ch, output_dim)
        # Embedding for projection discrimination
        #if not kwargs["agnostic_unet"] and not kwargs["unconditional"]:
        #    self.embed = self.which_embedding(self.n_classes, self.arch['out_channels'][-1]+extra)
        if not kwargs["unconditional"]:
            self.embed_middle = self.which_embedding(self.n_classes, 16*self.ch)
            self.embed = self.which_embedding(self.n_classes, self.arch['out_channels'][-1])

        # Initialize weights
        if not skip_init:
            self.init_weights()

        ###
        print("_____params______")
        for name, param in self.named_parameters():
            print(name, param.size())

        # Set up optimizer
        self.lr, self.B1, self.B2, self.adam_eps = D_lr, D_B1, D_B2, adam_eps
        if D_mixed_precision:
            print('Using fp16 adam in D...')
            import utils
            self.optim = utils.Adam16(params=self.parameters(), lr=self.lr,
                                                         betas=(self.B1, self.B2), weight_decay=0, eps=self.adam_eps)
        else:
            self.optim = optim.Adam(params=self.parameters(), lr=self.lr,
                                                         betas=(self.B1, self.B2), weight_decay=0, eps=self.adam_eps)
        # LR scheduling, left here for forward compatibility
        # self.lr_sched = {'itr' : 0}# if self.progressive else {}
        # self.j = 0

    # Initialize
    def init_weights(self):
        self.param_count = 0
        for module in self.modules():
            if (isinstance(module, nn.Conv2d)
                    or isinstance(module, nn.Linear)
                    or isinstance(module, nn.Embedding)):
                if self.init == 'ortho':
                    init.orthogonal_(module.weight)
                elif self.init == 'N02':
                    init.normal_(module.weight, 0, 0.02)
                elif self.init in ['glorot', 'xavier']:
                    init.xavier_uniform_(module.weight)
                else:
                    print('Init style not recognized...')
                self.param_count += sum([p.data.nelement() for p in module.parameters()])
        print('Param count for D''s initialized parameters: %d' % self.param_count)



    def forward(self, x, y=None):
        # Stick x into h for cleaner for loops without flow control
        h = x

        residual_features = []
        residual_features.append(x)
        # Loop over blocks

        for index, blocklist in enumerate(self.blocks[:-1]):
            if self.resolution == 128:
                if index==6 :
                    h = torch.cat((h,residual_features[4]),dim=1)
                elif index==7:
                    h = torch.cat((h,residual_features[3]),dim=1)
                elif index==8:#
                    h = torch.cat((h,residual_features[2]),dim=1)
                elif index==9:#
                    h = torch.cat((h,residual_features[1]),dim=1)

            if self.resolution == 256:
                if index==7:
                    h = torch.cat((h,residual_features[5]),dim=1)
                elif index==8:
                    h = torch.cat((h,residual_features[4]),dim=1)
                elif index==9:#
                    h = torch.cat((h,residual_features[3]),dim=1)
                elif index==10:#
                    h = torch.cat((h,residual_features[2]),dim=1)
                elif index==11:
                    h = torch.cat((h,residual_features[1]),dim=1)

            for block in blocklist:
                h = block(h)

            if index in self.save_features[:-1]:
                residual_features.append(h)

            if index==self.save_features[-1]:
                # Apply global sum pooling as in SN-GAN
                h_ = torch.sum(self.activation(h), [2, 3])
                # Get initial class-unconditional output
                bottleneck_out = self.linear_middle(h_)
                # Get projection of final featureset onto class vectors and add to evidence
                if self.unconditional:
                    projection = 0
                else:
                    # this is the bottleneck classifier c
                    emb_mid = self.embed_middle(y)
                    projection = torch.sum(emb_mid * h_, 1, keepdim=True)
                bottleneck_out = bottleneck_out + projection

        out = self.blocks[-1](h)

        if self.unconditional:
            proj = 0
        else:
            emb = self.embed(y)
            emb = emb.view(emb.size(0),emb.size(1),1,1).expand_as(h)
            proj = torch.sum(emb * h, 1, keepdim=True)
            ################
        out = out + proj

        out = out.view(out.size(0),1,self.resolution,self.resolution)

        return out, bottleneck_out

import os
from PIL import Image
import matplotlib.pyplot as plt

def generate_images_f(folder1, folder2, folder3):
    # Get the list of image files in the first folder
    image_files1 = [f for f in os.listdir(folder1) if f.endswith('.png')]

    # Check if there are matching images in the second and third folders
    matching_files = [f for f in image_files1 if os.path.exists(os.path.join(folder2, f)) and os.path.exists(os.path.join(folder3, f))]

    # Ensure there are matching images in all three folders
    if not matching_files:
        print("No matching image files found in all three folders.")
    else:
        for matching_file in matching_files:
            img1_path = os.path.join(folder1, matching_file)
            img2_path = os.path.join(folder2, matching_file)
            img3_path = os.path.join(folder3, matching_file)

            img1 = Image.open(img1_path)
            img2 = Image.open(img2_path)
            img3 = Image.open(img3_path)

            img1 = img1.convert('RGB')
            img2 = img2.convert('RGB')
            img3 = img3.convert('RGB')
            # Plot images side by side
            plt.figure(figsize=(12, 4))

            plt.subplot(1, 3, 1)
            plt.imshow(img1)
            plt.title('Input')
            plt.axis('off')

            plt.subplot(1, 3, 2)
            plt.imshow(img2)
            plt.title('Output')
            plt.axis('off')

            plt.subplot(1, 3, 3)
            plt.imshow(img3)
            plt.title('Target')
            plt.axis('off')

            plt.suptitle(f"Images: {matching_file}")
            plt.show()

# Example usage
inp = '/content/drive/MyDrive/without_buildings'
gen = '/content/drive/MyDrive/final_images'
targ = '/content/drive/MyDrive/grayscale_with_buildings'
#Trying the model on the test images
generate_images_f(inp,gen,targ)

import os
import cv2
from skimage.metrics import structural_similarity as ssim

# Define the source and target folder paths
source_folder_path = '/content/drive/MyDrive/grayscale_with_buildings'
target_folder_path = '/content/drive/MyDrive/processed_images_2'

# Get a list of all PNG files in the source and target folders
source_image_files = [os.path.join(source_folder_path, f) for f in os.listdir(source_folder_path) if f.endswith('.png')]
target_image_files = [os.path.join(target_folder_path, f) for f in os.listdir(target_folder_path) if f.endswith('.png')]

# Function to read, resize, and convert image to grayscale
def read_image(image_path):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (256, 256))  # Resize image to 256x256
    return cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Function to compare two images using SSIM
def compare_images(image1, image2):
    s = ssim(image1, image2)
    return s

# Compare each image in source folder with each image in target folder
for source_image_file in source_image_files:
    source_image = read_image(source_image_file)
    for target_image_file in target_image_files:
        target_image = read_image(target_image_file)
        similarity = compare_images(source_image, target_image)
        print(f"Similarity between {os.path.basename(source_image_file)} and {os.path.basename(target_image_file)}: {similarity:.4f}")

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

# Define the source and target folder paths
source_folder_path = '/content/drive/MyDrive/grayscale_with_buildings'
target_folder_path = '/content/drive/MyDrive/processed_images_2'

# Get a list of all PNG files in the source and target folders
source_image_files = [f for f in os.listdir(source_folder_path) if f.endswith('.png')]
target_image_files = [f for f in os.listdir(target_folder_path) if f.endswith('.png')]

# Function to read, resize, and convert image to grayscale
def read_image(image_path):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (256, 256))  # Resize image to 256x256
    return cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Function to compare two images using SSIM
def compare_images(image1, image2):
    s = ssim(image1, image2)
    return s

# Prepare for plotting
similarity_scores = []

# Compare images with the same names in the source and target folders
for source_image_file in source_image_files:
    if source_image_file in target_image_files:
        source_image_path = os.path.join(source_folder_path, source_image_file)
        target_image_path = os.path.join(target_folder_path, source_image_file)
        source_image = read_image(source_image_path)
        target_image = read_image(target_image_path)
        similarity = compare_images(source_image, target_image)
        similarity_scores.append((source_image_file, similarity))
        print(f"Similarity between {source_image_file} and {source_image_file}: {similarity:.4f}")

# Convert similarity scores to a numpy array for easier manipulation
similarity_scores = np.array(similarity_scores, dtype=[('filename', 'U256'), ('score', 'f4')])

# Plot the similarity scores
plt.figure(figsize=(10, 6))
plt.bar(range(len(similarity_scores)), similarity_scores['score'])

plt.xlabel('Generated Image')
plt.ylabel('SSIM Score')
plt.title('Structural Similarity Index (SSIM) between Images')
plt.show()

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

# Define the source and target folder paths
source_folder_path = '/content/drive/MyDrive/grayscale_with_buildings'
target_folder_path = '/content/drive/MyDrive/processed_images_2'

# Get a list of all PNG files in the source and target folders
source_image_files = [f for f in os.listdir(source_folder_path) if f.endswith('.png')]
target_image_files = [f for f in os.listdir(target_folder_path) if f.endswith('.png')]

# Function to read, resize, and convert image to grayscale
def read_image(image_path):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (256, 256))  # Resize image to 256x256
    return cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Function to compare two images using SSIM
def compare_images(image1, image2):
    s = ssim(image1, image2)
    return s

# Prepare for plotting
similarity_scores = []

# Threshold for similarity
similarity_threshold = 0.8

# Compare images with the same names in the source and target folders
for source_image_file in source_image_files:
    if source_image_file in target_image_files:
        source_image_path = os.path.join(source_folder_path, source_image_file)
        target_image_path = os.path.join(target_folder_path, source_image_file)
        source_image = read_image(source_image_path)
        target_image = read_image(target_image_path)
        similarity = compare_images(source_image, target_image)
        similarity_scores.append((source_image_file, similarity))
        print(f"Similarity between {source_image_file} and {source_image_file}: {similarity:.4f}")

# Convert similarity scores to a numpy array for easier manipulation
similarity_scores = np.array(similarity_scores, dtype=[('filename', 'U256'), ('score', 'f4')])

# Calculate accuracy for each image pair
accuracy_scores = [(filename, 1.0 if score >= similarity_threshold else 0.0) for filename, score in similarity_scores]
accuracy_scores = np.array(accuracy_scores, dtype=[('filename', 'U256'), ('accuracy', 'f4')])

# Plot the similarity scores and accuracy
plt.figure(figsize=(14, 7))

# Plotting SSIM scores
plt.subplot(1, 2, 1)
plt.bar(range(len(similarity_scores)), similarity_scores['score'])
plt.xticks(range(len(similarity_scores)), similarity_scores['filename'], rotation=90)
plt.xlabel('Image Filename')
plt.ylabel('SSIM Score')
plt.title('SSIM Scores between Images')

# Plotting accuracy scores
plt.subplot(1, 2, 2)
plt.bar(range(len(accuracy_scores)), accuracy_scores['accuracy'])
plt.xticks(range(len(accuracy_scores)), accuracy_scores['filename'], rotation=90)
plt.xlabel('Image')
plt.ylabel('Accuracy')
plt.title('Accuracy of Each Image')

plt.tight_layout()
plt.show()