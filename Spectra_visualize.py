import pandas as pd
import matplotlib.pyplot as plt


file_path = "/Users/Desktop/virs/Files/" #path to the folder containing ground spectra files 
output_path = "/Users/Desktop/virs/output/" #create an output folder

# give the file name corresponding to each spectra file
rock = ["rock", "group1_00002.sed"] #group1_00002.sed is the name of the spectra file that is collected using Spectroradiometer
soil_sample = ["soil_sample", "group1_00009.sed", "group1_00010.sed"]
spruce_needle = ["spruce_needle", "group1_00011.sed", "group1_00012.sed"]
fresh_snow = ["fresh_snow", "group1_00013.sed", "group1_00014.sed"]
old_snow = ["old_snow", "group1_00015.sed", "group1_00016.sed"]
more_snow_less_water = ["more_snow_less_water", "group1_00018.sed", "group1_00019.sed"]
less_snow_more_water = ["less_snow_more_water", "group1_00020.sed", "group1_00021.sed"]
water = ["water", "group1_00026.sed", "group1_00027.sed"]

items = [rock, soil_sample, spruce_needle, fresh_snow, old_snow, more_snow_less_water, less_snow_more_water, water]

dataframe = pd.DataFrame()
plt.figure(facecolor='white')
itemid = 1
for item in items:
    count = len(item) - 1
    num = 0
    tempdf= pd.DataFrame()
    sample_files=[]
    for sample in item[1:]:
        num = num + 1;
        files = pd.read_csv(file_path + sample, sep='\t', header = 27)
        files.columns = ['Radiance', 'c2', 'c3', 'Reflectance']
        dataframe[item[0] + "_Reflectance_" + str(num)] = files["Reflectance"]
        tempdf["Radiance"] = files["Radiance"]
        tempdf["c2_" + str(num)] = files["c2"]
        tempdf["c3_" + str(num)] = files["c3"]
        tempdf[item[0] + "_Reflectance_" + str(num)] = files["Reflectance"]
        sample_files.append(item[0] + "_Reflectance_" + str(num))
        if(num == count):
            tempdf["Mean_" + item[0] + "_Reflectance"] = dataframe[sample_files].mean(1)
            tempdf["Standard_deviation_" + item[0]] = dataframe[sample_files].std(1)
        tempdf = tempdf.reset_index()
        tempdf2 = tempdf[tempdf.index % 200 == 0]
    plot_wav = tempdf["index"]
    plot_wav2 = tempdf2["index"]
    plot_mean = tempdf["Mean_" + item[0] + "_Reflectance"]
    plot_mean2 = tempdf2["Mean_" + item[0] + "_Reflectance"]
    plt_std = tempdf["Standard_deviation_" + item[0]]
    plt_std2 = tempdf2["Standard_deviation_" + item[0]]
    plt.plot(plot_wav, plot_mean,label=item[0] + "(" + str(count) + ")")
    plt.errorbar(plot_wav2, plot_mean2, plt_std2, linestyle='None', marker='.', capsize=3)
    plt.title(item[0] + "- " + str(count) + " sample(s)", fontsize=8, fontweight='bold')
    plt.xlabel('Wavelength (nm)', fontsize=7)
    plt.ylabel('Reflectance (% of Light)', fontsize=7)
    plt.subplots_adjust(hspace=.5,wspace=.3)
    plt.tick_params(axis='both', which='major', labelsize=5)
    plt.tick_params(axis='both', which='minor', labelsize=5)
    plt.savefig(output_path + item[0] + '.png')
    plt.show()

    tempdf.to_csv(output_path + item[0] + '.csv', index=None, header=True)
    itemid+=1

