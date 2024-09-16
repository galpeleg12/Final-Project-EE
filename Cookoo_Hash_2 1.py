import random
import matplotlib.pyplot as plt
import hashlib

def single_run(size_of_table,utilization, num_of_mini_tables):

    SIZE_OF_MINI_TABLE = int(size_of_table/num_of_mini_tables)
    NUM_OF_ELEMENTS = int(size_of_table * utilization)
    table =[[None for i in range(SIZE_OF_MINI_TABLE)] for l in range(num_of_mini_tables)]
    dict_by_fullness=dict()# <how many cells are occupied>:<how many jumps it took to put that key>
    dict_by_jumps=dict() # <number of jumps>:<how many keys took that number of jumps to be inserted>
    max_jumps=0
    total_jumps=0
    old_chosen = None
    elements = [i for i in range(NUM_OF_ELEMENTS)]
    random.shuffle(elements)
#     print("start")
#     print(elements)
    for i in range(NUM_OF_ELEMENTS):
        tmp=1 #num of jumps done so far
        value = elements[i]
        #print("old_chosen is:",old_chosen, "index is:", i)
        key = calculate_keys_sha256(value,num_of_mini_tables,SIZE_OF_MINI_TABLE) #key=[h1(value),h2(value),h3(value),h4(value)]
            
        succed= False # false while a cell is not found for our key
        while(succed == False):
            for j in range(num_of_mini_tables):
#                 print("new for loop, value is "+str(value))        
                if(table[j][key[j]] == None and succed == False):
                    table[j][key[j]] = value
                    total_jumps+=tmp
                    if(tmp > max_jumps):
                        max_jumps = tmp
                    succed = True
                    old_chosen = None
#                     print(table)
                    break
            if (succed == False):
                chosen = random.Random().randint(0, num_of_mini_tables - 1)
                while (chosen == old_chosen):
                     chosen = random.Random().randint(0, num_of_mini_tables - 1)
                temp = table[chosen][key[chosen]]
#                 print("chosen is:",chosen)
#                 print("key is:",key)
#                 print("table is:",table)
#                 print("temp is:", temp)
                table[chosen][key[chosen]] = value
                value = temp
#                 print(table)
                key = calculate_keys_sha256(value,num_of_mini_tables,SIZE_OF_MINI_TABLE) #key=[h1(i),h2(i),h3(i),h4(i)]
#                 print("new key is:",key)
                tmp+=1
        
        
        dict_by_fullness[i]=tmp
        if(tmp not in dict_by_jumps):
            dict_by_jumps[tmp]=1
        else:
            dict_by_jumps[tmp]+=1

        #print(table , max_jumps,total_jumps/NUM_OF_ELEMENTS)
        #print(dict_by_fullness)
        #print(dict_by_jumps)
    return(dict_by_jumps,dict_by_fullness,max_jumps,total_jumps)



def calc_statistics(num_of_runs,size_of_table,utilization,num_of_mini_tables): #calculating statistics by averaging on num of runs
    absloute_max_jumps=0
    dict_by_jumps_avg,dict_by_fullness_avg,max_jumps_avg,total_jumps_avg=single_run(size_of_table,utilization,num_of_mini_tables)
    num_of_runs-=1
    absloute_max_jumps=max_jumps_avg
    for i in range(num_of_runs-1):
        dict_by_jumps_temp, dict_by_fullness_temp, max_jumps_temp, total_jumps_temp = single_run(size_of_table,utilization,num_of_mini_tables)
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
    
    with open(f'table_size_{size_of_table}_utilization_{utilization}_num_of_tables_{num_of_mini_tables}.txt', 'w') as file:
    # Write content to the file
        file.write(f'total_jumps_avg= {total_jumps_avg} ,max_jumps_avg= {max_jumps_avg} ,absloute_max_jumps= {absloute_max_jumps}'+'\n')
        
#     # Extract x and y values from the dictionary
#     x_values = list(dict_by_fullness_avg.keys())
#     y_values = list(dict_by_fullness_avg.values())
# 
#     # Create a line graph
#     plt.bar(x_values, y_values)
#     plt.xlim(min(x_values) , max(x_values) )
#     plt.ylim(min(y_values) , max(y_values) )
#     # Add labels and title
#     plt.xlabel('num of occupied cells')
#     plt.ylabel('average num of jumps to insert')
#     plt.title('average num of jumps to insert as a function of num of occupied cells')
#     plt.savefig(f'avg_num_of_jumps_as_fun_occ_cells_table_size_{size_of_table}_utilization_{utilization}.jpeg',format='jpeg')
#     # Show the graph
#     #plt.show()
# 
#     # Extract x and y values from the dictionary
#     x_values = list(dict_by_jumps_avg.keys())
#     y_values = list(dict_by_jumps_avg.values())
# 
#     # Create a line graph
#     plt.bar(x_values, y_values)
#     plt.xlim(min(x_values) , max(x_values) )
#     plt.ylim(min(y_values) , max(y_values) )
#     # Add labels and title
#     plt.xlabel('num of jumps')
#     plt.ylabel('average num of keys who jump this much')
#     plt.title('average num of jumps to insert as a function of num of keys that took that jumps to be inserted')
#     plt.savefig(f'avg_num_of_jumps_as_fun_of_keys_table_size_{size_of_table}_utilization_{utilization}.jpeg',format='jpeg')
# 
#     # Show the graph
#     #plt.show()
    

def calculate_keys_sha256(input_int, num_of_mini_tables,SIZE_OF_MINI_TABLE):
    # Convert the integer to bytes
    input_bytes = input_int.to_bytes((input_int.bit_length() + 7) // 8, 'big')
    
    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256(input_bytes).digest()
    
    # Convert the binary digest into a string of bits
    sha256_bits = ''.join(format(byte, '08b') for byte in sha256_hash)
    keylist =[]
    grid = int(256 / num_of_mini_tables)
    for i in range(num_of_mini_tables):
        key = int(sha256_bits[i*grid:(i+1)*grid],2)
        key = key % SIZE_OF_MINI_TABLE
        keylist.append(key)
    return (keylist)
        
# print(calc_statistics(1000,16,1,4))

sizes=[2**i for i in range (13,17)] #running over all possible sets of util and size
utils=[0.9]
table_nums = [4]
for size in sizes:
    for util in utils:
        for tables in table_nums:
            calc_statistics(100,size,util,tables)

