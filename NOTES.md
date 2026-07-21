# Stablecoin Depeg Risk — Project Notes

## Depeg definition (locked)
- **Primary (C):** an event = daily deviation below −5 × (rolling 30-day std of deviation),
  computed on past data only (shift(1)), negative deviations only, with a 5bps sigma floor
  to prevent hair-trigger thresholds in ultra-calm periods.
- **Robustness (A):** fixed −50bps threshold, run alongside to confirm findings don't
  depend on the definitional choice.
- Rationale: project goal is *early warning* (anomaly-for-this-coin), not *severity*
  (economic peg failure), so coin-relative beats a uniform threshold. C primary, A as check.

## Event study — 11 episodes, flow signature catalogue
Every flagged event maps to a nameable real-world crisis (no artifacts).

| Coin | Date | Crisis | Class | Flow signature | Lead/Lag |
|------|------|--------|-------|----------------|----------|
| USDC | 2023-03-12 | SVB reserve failure | existential | sustained outflow + weeks of post-event bleed | lead 1-2d |
| DAI  | 2023-03-11 | SVB via USDC collateral | existential | +14% inflow surge (PSM arb minting) | coincident |
| USDC | 2022-06-30 | 3AC/Celsius | severe | outflow | lead 2d |
| DAI  | 2022-07-01 | 3AC/Celsius | severe | violent churn (±1.2%) | lead 2d |
| USDT | 2022-07-01 | 3AC/Celsius | severe | outflow | lead 1-2d |
| USDT | 2022-05-11 | UST collapse contagion | severe | post-event outflow | LAG |
| USDT | 2023-11-22 | Binance DOJ settlement | moderate | inflows *despite* depeg | flows blind |
| USDC | 2023-10-03 | bull-run flow depeg | benign | quiet | none |
| DAI  | 2023-10-03 | bull-run flow depeg | benign | quiet | none |
| DAI  | 2024-07-05 | risk-off (Germany BTC/Mt.Gox) | moderate | mild churn, recurring dips | weak |
| USDT | 2024-07-05 | risk-off | moderate | mild churn | weak |

## Key findings
1. **Flows lead in slow-burn crises, lag in sudden ones.** 3AC (rumor-driven, weeks-long) →
   all 3 coins led. UST (public overnight collapse) → lag. Onset speed governs predictability.
2. **Flow signature is mechanism-specific.** Fiat-backed (USDC/USDT) → outflow.
   Crypto-backed (DAI) → churn / mint-surge. Same crisis, different fingerprints.
3. **The signal discriminates distress from noise.** Real crises scream in flows;
   benign flow-depegs stay quiet. This is what makes it modelable, not just a price mirror.
4. **Two crisis classes are flow-invisible:** contagion-inflow (DAI/SVB) and venue-scare
   (USDT/Binance), where supply *rises* during stress. Documented model blind spot.

## Feature engineering decisions (Week 3)
- Windows: 3-day AND 7-day flow features (let model choose; leads were 1-2d, signatures ~1wk).
- Features 1-8 in first pass. Feature 9 (deviation-flow divergence interaction) held in
  reserve — only add if simple model specifically fails the divergence cases (overfitting risk
  with only ~11 positives).
- Signed daily flow is too weak (churn cancels); need abs_supply_change (churn) and
  supply_change_3d (accelerating outflow vs. isolated bars).

## Leakage & causality guards (critical — interview material)
- Every rolling window shifted by 1 day (shift(1)) so no feature sees its own day.
- Any scaling fit on TRAIN slice only, applied to test. Never fit on full data.
- Label is strictly FUTURE: features at day T, label = "event in T+1..T+5". Never same-day.
- Train/test split by DATE, never random (time series — random split leaks future into past).
- Framing: flows are *associated with* elevated depeg risk, never *cause*. Model finds
  prediction, not mechanism.
- Confound to name: market-wide fear drives both flows and price; model may be a
  "scary crypto day" detector. Testable via SVB (coin-specific, calm market) — if it catches
  that, it's learning something stablecoin-specific.
- Survivorship: only surviving coins studied (no UST/dead coins); model learns "stress in
  coins that recover." Stated scope boundary, not a flaw.