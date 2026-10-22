def summarize(rounds):
    """Summarize a list of rounds for the dashboard header.

    Best and average score are based on 18-hole rounds only, because a
    9-hole score can't be compared with an 18-hole score.
    """
    full_rounds = [r for r in rounds if r["holes_played"] == 18]
    scores = [r["score_to_par"] for r in full_rounds]
    # An empty list is falsy: without the checks, min([]) would raise ValueError.
    return {
        "rounds": len(rounds),
        "full_rounds": len(full_rounds),
        "best_full_round": min(scores) if scores else None,
        "average_full_round": round(sum(scores) / len(scores), 1) if scores else None,
    }
