    def save_data(self):
        output_image = np.zeros([self.index_all.shape[0], 32, 32, 9])
        output_yield = np.zeros([self.index_all.shape[0]])
        output_year = np.zeros([self.index_all.shape[0]])
        output_locations = np.zeros([self.index_all.shape[0],2])
        output_index = np.zeros([self.index_all.shape[0],2])
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

            bin_seq = np.linspace(1, 4999, 33)
            image_temp = self.calc_histogram(image_temp, bin_seq ,32, 32, 9)
            image_temp[np.isnan(image_temp)] = 0
            # if np.sum(image_temp) < 250:
            #     print 'broken image', filename
            #     print np.isnan(image_temp)

            output_image[i, :] = image_temp
            output_yield[i] = self.data_yield[i, 3]
            output_year[i] = int(year)
            output_locations[i, 0] = longitude
            output_locations[i, 1] = latitude
            output_index[i,:] = np.array([int(loc1),int(loc2)])
            # print image_temp.shape
            print i,np.sum(image_temp),year,loc1,loc2
        np.savez(self.dir+'histogram_all_full.npz',
                 output_image=output_image,output_yield=output_yield,
                 output_year=output_year,output_locations=output_locations,output_index=output_index)
        print 'save done'
