min_batch_size = 7
max_batch_size = 18


def end_learning_session(
        items_correct,
        items_seen,
        total_time,
        current_batch_size,
        expected_time):

    accuracy = items_correct/items_seen
    avg_time = total_time/items_seen
    if accuracy >= 0.8:
        acc_pace = "high"
    elif accuracy >= 0.6:
        acc_pace = "medium"
    else:
        acc_pace = "low"
    if avg_time > expected_time:
        pace = "slow"
    elif avg_time < expected_time:
        pace = "fast"
    else:
        pace = "medium"
    if acc_pace == "high" and pace == "fast":
        learning_speed = "fast"
    elif acc_pace == "medium" and pace == "fast":
        learning_speed = "fast"
    elif acc_pace == "low":
        learning_speed = "slow"
    else:
        learning_speed = "medium"

    if accuracy < 0.5:
        next_batch_size = current_batch_size-3
    elif accuracy < 0.6:
        next_batch_size = current_batch_size-1
    elif learning_speed == "fast" and accuracy >= 0.8:
        next_batch_size = current_batch_size+5
    elif learning_speed == "fast" and accuracy >= 0.7:
        next_batch_size = current_batch_size+3
    elif learning_speed == "medium" and accuracy >= 0.8:
        next_batch_size = current_batch_size+1
    else:
        next_batch_size = current_batch_size

    if next_batch_size < min_batch_size:
        next_batch_size = min_batch_size
    elif next_batch_size > max_batch_size:
        next_batch_size = max_batch_size
    return next_batch_size
