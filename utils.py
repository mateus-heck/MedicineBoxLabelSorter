def measure_similarity(predicted):
    expected_format = ["NN:NN", "LNN/NN", "LNN/NN", "LNNLNNN"]
    if len(predicted) != len(expected_format) or len(predicted) == 0:
        return 0

    total_score = 0
    total_expected_chars = 0
    total_predicted_chars = 0

    for pred, exp in zip(predicted, expected_format):

        for p, e in zip(pred, exp):
            if e == 'N' and p.isdigit():
                total_score += 1
            elif e == 'L' and p.isalpha():
                total_score += 1
            elif e == p:
                total_score += 1
            else:
                total_score -= 1

            if e in ('N', 'L', 'X'):
                total_expected_chars += 1
            if p.isdigit() or p.isalpha():
                total_predicted_chars += 1
            if(len(pred) != len(exp)):
                total_score -= 0.31

    similarity = total_score / max(total_expected_chars, total_predicted_chars)
    return similarity


def replace_chars(predict):
    letter_mapping = {
        'S': '5',
        'o': '0',
        'O': '0',
        'l': '1',
        'U': 'V'
    }
    for i, pred in enumerate(predict):
        predict[i] = ''.join(letter_mapping.get(char, char) for char in pred)
    return predict