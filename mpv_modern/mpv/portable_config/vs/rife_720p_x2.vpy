### Rife v4, wypełnianie klatek, średnie wyagania wydajnościowe plik wyjściowy w 720p
### To samo co rife_2x.vpy !!!
##  input_uosc.conf:
#                  vf set vapoursynth="~~/vs/rife_720p_x2.vpy" ; show-text "Preset MVTools_2x"      #! Filtr Wideo > Preset RIFE_720p_x2

import vapoursynth as vs
from vapoursynth import core

input = video_in
colorlv = input.get_frame(0).props._ColorRange
fmt_fin = input.format.id

#####################
# Opcje Użytkownika #
#####################

FPS_multiply = 2
FPS_den = 1
GPU_ID = 0
GPU_THREAD = 8

## Wartość FPS_num/FPS_den to wielokrotność częstotliwości klatek (licznik i mianownik muszą być liczbami całkowitymi, a wynik obliczeń może być liczbą zmiennoprzecinkową; obsługiwane tylko w modelu v4) 2/1 = fps x 2
## .
## Numer karty graficznej używanej do przetwarzania, z 0 oznaczającym pierwszą kartę w kolejności
## Liczba wątków procesora karty graficznej, która ma być używana do przetwarzania (orginalnie = 2)

if container_fps > 32 :
	raise Exception("Częstotliwość klatek źródłowych przekracza dopuszczalny zakres, tymczasowo wyłączono ten skrypt.")

# Upewnij się, że wejście nie jest zduplikowaną ramką
sc_clip = core.misc.SCDetect(clip=input, threshold=0.15)

#                                 1280x720
if (input.width * input.height) > 921600:
	sc_clip = input.resize.Bicubic(width=1280, height=720, format=vs.RGBS, matrix_in_s="709")
else:
	sc_clip = input.resize.Bilinear(format=vs.RGBS, matrix_in_s="709")

interpolated = core.rife.RIFE(clip=sc_clip, model=9, factor_num=FPS_multiply, factor_den=FPS_den, gpu_id=GPU_ID, gpu_thread=GPU_THREAD, sc=True, skip=True, skip_threshold=60.0)

out = interpolated.resize.Bilinear(format=fmt_fin, matrix_s="709", range=1 if colorlv == 0 else None)

out.set_output()