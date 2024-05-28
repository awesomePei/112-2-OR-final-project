or i in B:
    for k in K:
        for delta in range(1, 7):
            if k + delta < len(K):
                model.addConstr(x[i, k] + x[i, k+delta] <= 1 + rep_penalty_x[i, k])

for i in F:
    for j in [1, 2]:
        for k in K:
            for delta in range(1, 7):
                if k + delta < len(K):
                    model.addConstr(y[i, j, k] + y[i, j, k+delta] <= 1 + rep_penalty_y[i, j, k])

for i in S:
    for j in [1, 2]:
        for k in K:
            for delta in range(1, 7):
                if k + delta < len(K):
      