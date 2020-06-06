from sklearn import metrics
preds=[0.2,0.4,0,0.4]
labels=[1,1,0,0]

print("sklearn res: {}".format(metrics.roc_auc_score(labels,preds)))

def custom_auc(labels_inp,preds_inp):
    pos_idx = [idx for idx,lbl in enumerate(labels_inp) if lbl==1]
    neg_idx = [idx for idx,lbl in enumerate(labels_inp) if lbl==0]
    # 所有的组合情况
    total_cnt = len(pos_idx)*len(neg_idx)
    # 所有满足要求的组合 | 负样本的分数 < 正样本的分数
    satisfied_cnt = 0
    for pidx in pos_idx:
        for nidx in neg_idx:
            if preds_inp[nidx] < preds_inp[pidx]:
                satisfied_cnt += 1
            elif preds_inp[nidx] == preds_inp[pidx]:
                # 从排序来看，相等的时候排序就是随机排了，AB BA都可能
                # 只有1/2的概率会排出正确的结果
                satisfied_cnt += 0.5
            else:
                satisfied_cnt += 0
    return 1.0*satisfied_cnt/total_cnt

print("custom_auc res: {}".format(custom_auc(labels,preds)))


