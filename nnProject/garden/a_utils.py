#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/06/22 1:52 AM
import numpy as np
import pandas as pd


def trans():
    data = pd.read_csv('seed.csv')

    seed_pd = pd.DataFrame(columns=['Index', 'Issue', 'Red', 'Blue'])
    for i in range(len(data)):
        index = data.loc[i]['Index']
        issue = data.loc[i]['Issue']
        red = [data.loc[i]['a'], data.loc[i]['b'], data.loc[i]['c'], data.loc[i]['d'], data.loc[i]['e']]
        blue = [data.loc[i]['m'], data.loc[i]['n']]

        new = pd.DataFrame(columns=['Index', 'Issue', 'Red', 'Blue'])
        new.loc[i] = {'Index': index,
                      'Issue': issue,
                      'Red': red,
                      'Blue': blue}
        seed_pd = pd.concat([seed_pd, new], sort=False)

    seed_pd.to_csv('new_seed.csv')
    print('==========================================================')
    print(seed_pd)


if __name__ == '__main__':
    trans()