import random
import matplotlib.pyplot as plt
size_of_table =2048
utilization=0.8 #precentage of table final fullness
ORIG_SIZE_OF_TABLE = 2048
UTILIZATION = 1
SIZE_OF_TABLE = int(ORIG_SIZE_OF_TABLE * UTILIZATION)
C1 = 0.5
C2 = 0.5
def single_run(size_of_table,utilization):
#try to check for a 0.8size , 0.6size ... and check for the utilization
#can run a loop that grabs the max utilization

    NUM_OF_ELEMENTS = int(size_of_table * utilization)
    table =[None for i in range(size_of_table)]
    dict_by_fullness=dict()# <how many cells are occupied>:<how many jumps it took to put that key>
    dict_by_jumps=dict() # <number of jumps>:<how many keys took that number of jumps to be inserted>
    max_jumps=0
    total_jumps=0
    for i in range(NUM_OF_ELEMENTS):
        tmp=1
        key = random.Random().randint(0, size_of_table-1) #key=h(i)
        base_key = key
        succed= False # false while a cell is not found for our key
        while(succed == False):
            if(table[key] == None):
                table[key] = i
                total_jumps+=tmp
                if(tmp > max_jumps):
                    max_jumps = tmp
                succed = True
            else:
                key=(int(base_key + C1*tmp + C2 * tmp * tmp))%size_of_table
                #print(key)
                tmp+=1
        dict_by_fullness[i]=tmp
        if(tmp not in dict_by_jumps):
            dict_by_jumps[tmp]=1
        else:
            dict_by_jumps[tmp]+=1

        #print(table , max_jumps,total_jumps/SIZE_OF_TABLE)
        #print(dict_by_fullness)
        #print(dict_by_jumps)
    return(dict_by_jumps,dict_by_fullness,max_jumps,total_jumps)



def calc_statistics(num_of_runs,size_of_table,utilization): #calculating statistics by averaging on num of runs
    absloute_max_jumps=0
    dict_by_jumps_avg,dict_by_fullness_avg,max_jumps_avg,total_jumps_avg=single_run(size_of_table,utilization)
    num_of_runs-=1
    absloute_max_jumps=max_jumps_avg
    for i in range(num_of_runs-1):
        dict_by_jumps_temp, dict_by_fullness_temp, max_jumps_temp, total_jumps_temp = single_run(size_of_table,utilization)
        total_jumps_avg+=total_jumps_temp
        max_jumps_avg+=max_jumps_temp
        if(max_jumps_temp>absloute_max_jumps):
            absloute_max_jumps=max_jumps_temp
        for key in dict_by_fullness_temp.keys():
            dict_by_fullness_avg[key] += dict_by_fullness_temp[key]
        for key in dict_by_jumps_temp.keys():
            if key not in  dict_by_jumps_avg:
                dict_by_jumps_avg[key] = dict_by_jumps_temp[key]
            else:
                dict_by_jumps_avg[key] += dict_by_jumps_temp[key]

    total_jumps_avg = total_jumps_avg / (num_of_runs * size_of_table*utilization)
    max_jumps_avg = max_jumps_avg / (num_of_runs)
    for key in dict_by_fullness_avg.keys():
        dict_by_fullness_avg[key] = dict_by_fullness_avg[key] / (num_of_runs)
    for key in dict_by_jumps_avg.keys():
        dict_by_jumps_avg[key] = dict_by_jumps_avg[key] / (num_of_runs)
    
    with open(f'table_size_{size_of_table}_utilization_{utilization}.txt', 'w') as file:
    # Write content to the file
        file.write(f'total_jumps_avg= {total_jumps_avg} ,max_jumps_avg= {max_jumps_avg} ,absloute_max_jumps= {absloute_max_jumps}'+'\n')
    # Extract x and y values from the dictionary
    x_values = list(dict_by_fullness_avg.keys())
    y_values = list(dict_by_fullness_avg.values())

    # Create a line graph
    plt.bar(x_values, y_values)
    plt.xlim(min(x_values) , max(x_values) )
    plt.ylim(min(y_values) , max(y_values) )
    # Add labels and title
    plt.xlabel('num of occupied cells')
    plt.ylabel('average num of jumps to insert')
    plt.title('average num of jumps to insert as a function of num of occupied cells')
    plt.savefig(f'avg_num_of_jumps_as_fun_occ_cells_table_size_{size_of_table}_utilization_{utilization}.jpeg',format='jpeg')
    # Show the graph
    #plt.show()

    # Extract x and y values from the dictionary
    x_values = list(dict_by_jumps_avg.keys())
    y_values = list(dict_by_jumps_avg.values())

    # Create a line graph
    plt.bar(x_values, y_values)
    plt.xlim(min(x_values) , max(x_values) )
    plt.ylim(min(y_values) , max(y_values) )
    # Add labels and title
    plt.xlabel('num of jumps')
    plt.ylabel('average num of keys who jump this much')
    plt.title('average num of jumps to insert as a function of num of keys that took that jumps to be inserted')
    plt.savefig(f'avg_num_of_jumps_as_fun_of_keys_table_size_{size_of_table}_utilization_{utilization}.jpeg',format='jpeg')

    # Show the graph
    #plt.show()
sizes=[2**i for i in range (10,17)] #running over all possible sets of util and size
utils=[0.6,0.7,0.8,0.9,1]
for size in sizes:
    for util in utils:
        calc_statistics(1000,size,util)
