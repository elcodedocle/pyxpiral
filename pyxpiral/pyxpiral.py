#!/usr/bin/env python
"""
pyxpiral.py - Pseudo-DataMatrix (de)coder.
"""

import argparse
import operator
import math
import io
import binascii
import sys
import numpy
from PIL import Image

if sys.version_info < (3, 0):
	from fractions import gcd
else:
	from math import gcd


class Pyxpiral(object):
	"""Turns any ascii string into a 2d bitmap + animated gif and vice-versa.
	"""

	def __init__(self):
		pass

	@staticmethod
	def _get_bits_from_msg(message):
		return bin(int(binascii.hexlify(message if sys.version_info < (3, 0) else bytes(message,'ascii')), base=16))[2:]+'1'

	@staticmethod
	def _get_dim(size):
		return int(math.ceil(math.sqrt(size)))

	@staticmethod
	def _get_offset(dim):
		return int(math.ceil((dim-1)//2))

	@staticmethod
	def _array_to_image(msg_matrix):
		image = Image.fromarray(numpy.array(msg_matrix))
		if image.mode != 'RGB':
			image = image.convert('RGB')
		return image

	@staticmethod
	def _image_to_array(input_filename, downscale=10):
		image = Image.open(input_filename)
		image.load()
		image = image.resize([x//downscale for x in image.size])
		return numpy.asarray(image, dtype="int32")

	@staticmethod
	def _array_to_bits(image_matrix, bg_color=0x00, step_size=1, ld_border=1):
		xpsize = int(math.pow(len(image_matrix),2))
		dim = Pyxpiral._get_dim(xpsize)
		offset = Pyxpiral._get_offset(dim)
		offset_cur = [offset-ld_border,offset]
		bits = []
		for cur in Pyxpiral._get_cursor(xpsize, offset_cur, step_size):
			bits.append('0' if str(image_matrix[cur[0]][cur[1]][0])==str(bg_color) else '1')
		return ''.join(bits).rstrip('0')[:-1]

	@staticmethod
	def _bits_to_ascii(bits, encoding='ascii', errors='replace'):
		i = int(bits, 2)
		hex_string = '%x' % i
		n = len(hex_string)
		return binascii.unhexlify(hex_string.zfill(n + (n & 1))).decode(encoding, errors)

	@staticmethod
	def _get_cursor(xpiral_size, offset_cursor=[0,0], step_size=1):
		cur = offset_cursor
		refs = [1,1]
		movs = [[step_size,0],[0,step_size],[-step_size,0],[0,-step_size]]
		i = 0
		j = 0
		k = 0
		while i < xpiral_size:
			yield cur
			cur = list(map(operator.add, cur, movs[j]))
			if k==0:
				refs[j%2] += 1
				j = (j+1)%len(movs)
			k = (k+1)%refs[j%2]
			i += 1

	@staticmethod
	def _pixpiralize(bits, bits_color=0xFF, bg_color=0x00, step_size=1, ld_border=1):
		xpsize = len(bits)
		dim = Pyxpiral._get_dim(xpsize*step_size)
		bit_matrix = [[bg_color for x in range(dim+ld_border)] for y in range(dim+ld_border)]
		offset = Pyxpiral._get_offset(dim)
		offset_cur = [offset,offset+ld_border]
		i = 0
		for cur in Pyxpiral._get_cursor(xpsize, offset_cur, step_size):
			bit_matrix[cur[0]][cur[1]] = int(bits[i])*bits_color
			i += 1
		return bit_matrix

	@staticmethod
	def encode(msg, upscale=10, bits_color=0xFF, bg_color=0x00, step_size=1, ld_border=1):
		"""Encodes ascii message into BMP image.

		Args:
			msg (str): Message to encode.
			upscale (int, default=10): bit size in square pixels
			bits_color (int, default=0xFF): color for bit value 1
			bg_color (int, default=0x00): color for bit value 0
			step_size (int, default=1): distance between consecutive bits
			ld_border (int, default=1): distance between consecutive bits

		Returns:
			(PIL.Image): An image object from Pillow library 
		"""
		bits = Pyxpiral._get_bits_from_msg(msg)
		msg_matrix = Pyxpiral._pixpiralize(
			bits,
			bits_color=bits_color,
			bg_color=bg_color,
			step_size=step_size
		)
		image = Pyxpiral._array_to_image(msg_matrix)
		return image.resize([x*upscale for x in image.size])

	@staticmethod
	def encode_fractal(msg, upscale=10, colors=[0xFF,0x00], step_size=1, rotation_step = 1):
		"""Encodes ascii message into GIF animated image sequence.

		Args:
			msg (str): Message to encode.
			upscale (int, default=10): bit size in square pixels
			colors (list, default=[0xFF,0x00]): list [color for bit value 1 (int), color for bit value 0 (int)]
			step_size (int, default=1): distance between consecutive bits
			rotation_step (int, default=1): bits rotated per gif frame

		Returns:
			(list): A list of PIL.Image image objects from Pillow library 
		"""
		bits = Pyxpiral._get_bits_from_msg(msg)
		num_rotations = int(len(bits)//gcd(len(bits),rotation_step))
		msg_img_seq = []
		for _ in range(num_rotations):
			image = Pyxpiral._array_to_image(
				Pyxpiral._pixpiralize(
					bits,
					bits_color=colors[0],
					bg_color=colors[1],
					step_size=step_size
				)
			)
			image = image.resize([x*upscale for x in image.size])
			msg_img_seq.append(image)
			bits = bits[-rotation_step-1:-1] + bits[:-rotation_step-1] + '1'
		return msg_img_seq

	@staticmethod
	def decode(filename, downscale=10, bg_color=0x00, step_size=1):
		"""Decodes ascii message from BMP image.

		Args:
			filename (str): source BMP image filename.
			downscale (int, default=10): bit size in square pixels
			bg_color (int, default=0x00): color for bit value 0
			step_size (int, default=1): distance between consecutive bits

		Returns:
			(str): Decoded ascii string message
		"""
		image_array = Pyxpiral._image_to_array(filename, downscale=downscale)
		bits = Pyxpiral._array_to_bits(image_array, bg_color=bg_color, step_size=step_size)
		return Pyxpiral._bits_to_ascii(bits)


def main(argv):
	"""Processes the program input arguments for turning any ascii string into a 2d bitmap or gif and vice-versa.

		Args:
			argv (list): list of str containing the program input arguments.
	"""

	parser = argparse.ArgumentParser(description='Pseudo-DataMatrix (de)coder with no practical use. Turns any ascii string into a 2d bitmap + animated gif and vice-versa.')

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--encode', help='message to encode')
	group.add_argument('--decode', default=False, type=argparse.FileType('rb'), help='image to decode')

	parser.add_argument('--scale', default=10, type=int, help='bit size in square pixels, default=10')
	parser.add_argument('--bg-color', default=0x00, type=int, help='bit color for value 0, default=0x00')
	parser.add_argument('--bits-color', default=0xFF, type=int, help='bit color for value 1, default=0xFF')
	parser.add_argument('--step-size', default=1, type=int, help='distance between consecutive bits, default=1')
	parser.add_argument('--rotation-step', default=1, type=int, help='bits rotated per gif frame, default=1')
	parser.add_argument('--frame-duration', default=100, type=int, help='frame duration in ms, default=100')
	parser.add_argument('--loops', default=0, type=int, help='number of gif loops (0=infinite), default=0')
	
	parser.add_argument('--output-filename', default=None, type=argparse.FileType('wb'), help='output filename (.gif will be appended on gif generation)')

	args = parser.parse_args(argv[1:])

	# Pyxpiral is static, instance is not required.
	ppl = Pyxpiral()

	if args.decode:
		msg = ppl.decode(args.decode, args.scale, args.bg_color, args.step_size)
		print('Decoded' + args.decode.name + ': ' + msg)
		return

	if not args.output_filename:
		args.output_filename = open('output.bmp','w')

	image = ppl.encode(
		args.encode,
		upscale=args.scale,
		bits_color=args.bits_color,
		bg_color=args.bg_color,
		step_size=args.step_size
	)

	image.save(args.output_filename.name, format='BMP')

	msg_img_seq = ppl.encode_fractal(
		args.encode,
		upscale=args.scale,
		colors=[
			args.bits_color,
			args.bg_color
		],
		step_size=args.step_size,
		rotation_step = args.rotation_step
	)

	msg_img_seq[0].save(
		args.output_filename.name+'.gif',
		save_all=True,
		append_images=msg_img_seq[1:],
		duration=args.frame_duration,
		loop=args.loops
	)

	print('Generated ' + args.output_filename.name + ' and ' + args.output_filename.name + '.gif')


if __name__ == "__main__":
	main(sys.argv)