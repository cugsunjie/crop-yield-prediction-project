    def save_data(self):
        output_image = np.zeros([count_max, 32, 32, 9])
        output_yield = np.zeros([count_max])
        output_year = np.zeros([count_max])
        output_locations = np.zeros([count_max,2])
        output_index = np.zeros([count_max,2])
        for i in self.index_all:
            year = str(int(self.data_yield[i, 0]))
            loc1 = str(int(self.data_yield[i, 1]))
            loc2 = str(int(self.data_yield[i, 2]))

            key = np.array([int(loc1),int(loc2)])
            index = np.where(np.all(self.locations[:,0:2].astype('int') == key, axis=1))
            longitude = self.locations[index,2]
            latitude = self.locations[index,3]

            filename = year + '_' + loc1 + '_' + loc2 + '.npy'
            image_temp = np.load(self.dir + filename)
            image_temp = self.filter_timespan(image_temp, 49, 305, 9)

            image_temp=np.reshape(image_temp,(image_temp.shape[0]*image_temp.shape[1],image_temp.shape[2]),order='C')
            # remove 0 and 5000
            image_temp[image_temp==5000]=0
            # image_temp = image_temp[np.all(image_temp, axis=1)]
            image_temp = image_temp[~np.all(image_temp == 0, axis=1)]
            # print image_temp.shape

            crop_pixel_count = 200
            j = 0
            while j < image_temp.shape[0]/crop_pixel_count:
                image_temp_part = image_temp[j*crop_pixel_count:(j+1)*crop_pixel_count,:]
                j += 1
                bin_seq = np.linspace(1, 4999, 33)
                image_temp_part = self.calc_histogram_flat(image_temp_part, bin_seq,32, 32, 9)
                image_temp_part[np.isnan(image_temp_part)] = 0
                # if np.sum(image_temp_part) < 288:
                #     print 'broken image', filename, np.sum(image_temp_part)
                #     continue

                epoch = count/count_max
                #saver
                if count%count_max == 0 and count!=0:
                    # save
                    np.savez(self.dir+'histogram_semi_rand_200_20000'+str(epoch)+'.npz',
                         output_image=output_image,output_yield=output_yield,
                         output_year=output_year,output_locations=output_locations,output_index=output_index)
                    print 'save',self.dir+'histogram_semi_rand_200_20000'+str(epoch)+'.npz'
                    # clear
                    output_image = np.zeros([count_max, 32, 32, 9])
                    output_yield = np.zeros([count_max])
                    output_year = np.zeros([count_max])
                    output_locations = np.zeros([count_max,2])
                    output_index = np.zeros([count_max,2])

                output_image[count-epoch*count_max, :] = image_temp_part
                output_yield[count-epoch*count_max] = self.data_yield[i, 3]
                output_year[count-epoch*count_max] = int(year)
                output_locations[count-epoch*count_max, 0] = longitude
                output_locations[count-epoch*count_max, 1] = latitude
                output_index[count-epoch*count_max,:] = np.array([int(loc1),int(loc2)])
                print epoch,i,j,count,np.sum(image_temp_part),year,loc1,loc2
                count += 1
        print 'save done'
