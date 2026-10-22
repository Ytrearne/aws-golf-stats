def summarize(rounds):
    full_rounds = [r for r in rounds if r["holes_played"] == 18]
    scores = [r["score_to_par"] for r in full_rounds]
    return {
        "rounds": len(rounds),
        "full_rounds": len(full_rounds),
        "best_full_round": min(scores) if scores else None,
        "average_full_round": round(sum(scores) / len(scores), 1) if scores else None,
    }
