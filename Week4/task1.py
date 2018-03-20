import cv2
import matplotlib.pyplot as plt
import numpy as np
import warnings

data_path = '../../databases'
PlotsDirectory = '../plots/Week4/task1/'

def task1(gt, test, offset):
    gtx = (np.array(gt[:, :, 1], dtype=float) - (2 ** 15)) / 64.0
    gty = (np.array(gt[:, :, 2], dtype=float) - (2 ** 15)) / 64.0
    gtz = np.array(gt[:, :, 0], dtype=bool)
    print("non ocluded gt:" + str(np.count_nonzero(gtz)))


    testx = (np.array(test[:, :, 1], dtype=float))/offset
    testy = (np.array(test[:, :, 2], dtype=float))/offset
    testz = np.array(test[:, :, 0], dtype=bool)
    print("non ocluded test:" + str(np.count_nonzero(testz)))

    mask1 = np.logical_and(gtz, testz)

    validPixels = np.count_nonzero(mask1)
    print("Valid pixels "+str(validPixels))
    if np.count_nonzero(mask1) < int(0.2*np.prod(gt.shape)):
        warnings.warn("Low number of valid pixels")

    gtx_1 = gtx * mask1
    gty_1 = gty * mask1
    testx_1 = testx * mask1
    testy_1 = testy * mask1

    # Mean Square error in Non-ocluded areas
    msen = np.sqrt((gtx_1 - testx_1) ** 2 + (gty_1 - testy_1) ** 2)
    msen_r = np.reshape(msen, [-1])[np.reshape(mask1, [-1])]

    # plt.figure(1)
    # plt.hist(msen_r, bins=50, normed=True)
    # plt.title("MSE normalized histogram")
    # plt.ylabel("% pixels")
    # plt.xlabel("MSE")

    m_msen = np.mean(np.mean(msen_r))
    print("x2mean square error (non-ocluded): " + str(m_msen))

    # plt.figure(2)
    # plt.imshow(msen)
    # plt.colorbar()
    # plt.title("MSE map")

    mask2 = msen > 3.0


    # Percentage of Erroneous Pixels in Non-occluded areas
    pepn = np.count_nonzero(mask1[mask2]) / np.count_nonzero(mask1)
    print("percentage of erroneous pixels (non-ocluded): " + str(pepn) + "\n")


    return m_msen, pepn

def gunner_farneback(prvs, act):

    hsv = np.zeros_like(prvs)
    hsv[..., 1] = 255

    flow = cv2.calcOpticalFlowFarneback(prvs, act, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('frame2', bgr)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png', frame2)
        cv2.imwrite('opticalhsv.png', bgr)
    cap.release()
    cv2.destroyAllWindows()
    return opt_flow

def evaluate_custom(seq, dataset, names):
    # area_offsets = np.arange(1, 65, 7)
    # block_dims = np.arange(2, 33, 6)
    area_offsets = [32]
    block_dims = [8]

    gt = cv2.imread(names[0], -1)
    prvs = cv2.imread(names[1], 0)
    next = cv2.imread(names[2], 0)
    block_list_p, block_list_m, list_m, list_p = [], [], [], []
    combinations = len(block_dims)*len(area_offsets)

    for i, block in enumerate(block_dims):
        for j, offset in enumerate(area_offsets):
            print("Computing "+str(i+j)+"/"+str(combinations))
            opt_flow = # Todo: Receive gt[x,y,z] block matching from test image
            m_msen, pepn = task1(gt, opt_flow, offset)
            list_m.append(m_msen)
            list_p.append(pepn)
        block_list_m.append(list_m)
        block_list_p.append(list_p)

    # Plot 2x mean square error vs areas offsets
    plotlines(block_list_m, area_offsets, block_dims, "MMSE", seq, dataset)

    # Plot percentage of erroneous pixels in non-occluded vs areas offsets
    plotlines(block_list_p, area_offsets, block_dims, "PEPN", seq, dataset)

    # Find best mmse
    best_mmse = best_evaluation(block_list_m, "maximum")

    # Find best pepn
    best_pepn = best_evaluation(block_list_p, "minimum")

    return best_mmse, best_pepn

def evaluate_gunner_farneback(seq, dataset, names):
    gt = cv2.imread(names[0], -1)
    prvs = cv2.imread(names[1], 0)
    next = cv2.imread(names[2], 0)


    block_list_p, block_list_m, list_m, list_p = [], [], [], []
    combinations = len(block_dims) * len(area_offsets)

    for i, block in enumerate(block_dims):
        for j, offset in enumerate(area_offsets):
            print("Computing " + str(i + j) + "/" + str(combinations))
            opt_flow = gunner_farneback()
            m_msen, pepn = task1(gt, opt_flow, offset)
            list_m.append(m_msen)
            list_p.append(pepn)
        block_list_m.append(list_m)
        block_list_p.append(list_p)

    # Plot 2x mean square error vs areas offsets
    #plotlines(block_list_m, area_offsets, block_dims, "MMSE", seq, dataset)

    # Plot percentage of erroneous pixels in non-occluded vs areas offsets
    #plotlines(block_list_p, area_offsets, block_dims, "PEPN", seq, dataset)

    # Find best mmse
    best_mmse = best_evaluation(block_list_m, "maximum")

    # Find best pepn
    best_pepn = best_evaluation(block_list_p, "minimum")

    return best_mmse, best_pepn

def best_evaluation(evaluations, criteria):
    best = evaluations[0][0]
    for listeval in evaluations:
        for value in listeval:
            if criteria[:3] == "max":
                if best < value:
                    best = value
            elif criteria[:3] == "min":
                if best > value:
                    best = value
    return best


def plotlines(list_values, area_offsets, blocks, title, seq, dataset):
    plt.figure()
    lines = []
    for lv, block in zip(list_values, blocks):
        line, = plt.plot(lv, area_offsets, 'k', label=' = ' + str(block))
        lines.append(line)
    plt.title(title+" " + seq + " sequence]")
    plt.xlabel("Area of search")
    plt.ylabel(title)
    plt.legend(handles=lines, loc='upper center', bbox_to_anchor=(0.5, -0.1))
    plt.savefig(PlotsDirectory + dataset + '_sequence' + seq + '.png', bbox_inches='tight')
    plt.close()

    return

if __name__ == "__main__":
    # First pair
    gt45_name = "../../databases/data_stereo_flow/training/flow_noc/000045_10.png"
    test45_name1 = "../../databases/data_stereo_flow/training/image_0/000045_10.png"
    test45_name2 = "../../databases/data_stereo_flow/training/image_0/000045_11.png"
    names45 = [gt45_name, test45_name1, test45_name2]

    # Second pair
    gt157_name = "../../databases/data_stereo_flow/training/flow_noc/000157_10.png"
    test157_name1 = "../../databases/data_stereo_flow/training/image_0/000157_10.png"
    test157_name2 = "../../databases/data_stereo_flow/training/image_0/000157_11.png"
    names157 = [gt157_name, test157_name1, test157_name2]

    best_mmse, best_pepn = evaluate_custom("45", "KITTI", names157)
    best_mmse, best_pepn = evaluate_gunner_farneback("45", "KITTI", names157)