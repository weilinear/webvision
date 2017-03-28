# Binary to run various functions.

from __future__ import print_function
import argparse
import config
import eval

if __name__ == '__main__':
    # Parse the args
    parser = argparse.ArgumentParser(description='Utilities for webvision challenge.')
    parser.add_argument('--validate', help='increase output verbosity', action="store_true")
    parser.add_argument('--eval_val', help='evaluate validation dataset')
    parser.add_argument('--top_k', help='top k evaluation', type=int)
    args = parser.parse_args()
    data_info = config.LoadInfo()
    if args.validate:
        print('Validating the data integrity.')
        if config.ValidateIntegrity(data_info):
            print ('Dataset Integrity Validated.')
    if args.eval_val:
        top_k = 5
        if args.top_k:
            top_k = args.top_k
        merged_df = eval.MergeValFile(data_info, args.eval_val)
        print ("Top %d accurarcy is %0.3f."%(
            top_k, eval.TopK(merged_df, top_k)))
        
