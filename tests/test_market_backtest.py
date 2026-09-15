from evolution.market_backtest import run_sma_cross,walk_forward

def bars(n=300):
    out=[]
    for i in range(n):
        c=100+i*.05+(i%11)*.02
        out.append({'open':c-.02,'high':c+.1,'low':c-.1,'close':c})
    return out

def test_backtest_metrics_are_bounded():
    r=run_sma_cross(bars(),5,20)
    assert r['trades']>=1
    assert 0<=r['win_rate']<=1
    assert 0<=r['max_drawdown']<=1

def test_walk_forward_has_unseen_test():
    r=walk_forward(bars(),fast=5,slow=20)
    assert 'train' in r and 'test' in r and 'test_score' in r
