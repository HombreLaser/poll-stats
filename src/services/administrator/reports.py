def response_score_count(responses):
    counts = build_dictionary(responses[0].data)

    for response in responses[1:]:
        for response_data in response.data:
            if response_data['type'] == 'open':
                continue

            counts[response_data['question']] = counts_dictionary(
                response_data['response'],
                counts=counts[response_data['question']]
            )

    return counts


def build_dictionary(response_data: list):
    counts = {}

    for response in response_data:
        if response['type'] == 'open':
            continue

        counts[response['question']] = counts_dictionary(response['response'])

    return counts


def counts_dictionary(response: dict, counts=None):
    if counts is None:
        dictionary = {'zero': 0, 'low': 0, 'medium': 0, 'high': 0}
    else:
        dictionary = counts

    match response['score']:
        case '0.0':
            dictionary['zero'] += 1
        case '0.3':
            dictionary['low'] += 1
        case '0.6':
            dictionary['medium'] += 1
        case '1.0':
            dictionary['high'] += 1

    return dictionary
