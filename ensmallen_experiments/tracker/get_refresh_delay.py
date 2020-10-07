def get_refresh_delay(elapsed: float) -> float:
    if elapsed < 0.01:
        return 0
    if elapsed < 0.1:
        return 0.00001
    if elapsed < 1:
        return 0.01
    if elapsed < 10:
        return 0.1
    if elapsed < 60:
        return 1
    if elapsed < 60*10:
        return 30
    if elapsed < 60*60:
        return 60
    return 60*3