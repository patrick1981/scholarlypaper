#!/usr/bin/env python3
"""
TDT 1000-Session Stabilization Analysis
Simulates token degradation over 1000 sessions to find stabilization point
Date: 2025-09-12
Uses combined Claude.ai and ChatGPT session data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import exp
try:
    from scipy import stats
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

# Matplotlib: minimal, portable defaults
plt.rcParams.update({
    "figure.figsize": (20, 12),
    "axes.grid": True,
    "grid.alpha": 0.3
})

class TDTStabilizationSimulator:
    def __init__(self):
        # Load observed 38-session data
        self.observed_data = self.load_observed_data()
        
    def load_observed_data(self):
        """Load the 38-session dataset"""
        data = [
            {'session': 1, 'tdt': 65}, {'session': 2, 'tdt': 70}, {'session': 3, 'tdt': 76},
            {'session': 4, 'tdt': 70}, {'session': 5, 'tdt': 99}, {'session': 6, 'tdt': 42},
            {'session': 7, 'tdt': 85}, {'session': 8, 'tdt': 89}, {'session': 9, 'tdt': 90},
            {'session': 10, 'tdt': 75}, {'session': 11, 'tdt': 80}, {'session': 12, 'tdt': 75},
            {'session': 13, 'tdt': 80}, {'session': 14, 'tdt': 70}, {'session': 15, 'tdt': 65},
            {'session': 16, 'tdt': 75}, {'session': 17, 'tdt': 75}, {'session': 18, 'tdt': 90},
            {'session': 19, 'tdt': 75}, {'session': 20, 'tdt': 75}, {'session': 21, 'tdt': 75},
            {'session': 22, 'tdt': 70}, {'session': 23, 'tdt': 85}, {'session': 24, 'tdt': 90},
            {'session': 25, 'tdt': 93}, {'session': 26, 'tdt': 75}, {'session': 27, 'tdt': 70},
            {'session': 28, 'tdt': 80}, {'session': 29, 'tdt': 85}, {'session': 30, 'tdt': 90},
            {'session': 31, 'tdt': 70}, {'session': 32, 'tdt': 75}, {'session': 33, 'tdt': 80},
            {'session': 34, 'tdt': 85}, {'session': 35, 'tdt': 70}, {'session': 36, 'tdt': 95},
            {'session': 37, 'tdt': 85}, {'session': 38, 'tdt': 75}
        ]
        return pd.DataFrame(data)
    
    @staticmethod
    def _rolling_slope(x, y):
        if HAVE_SCIPY:
            from scipy import stats
            return stats.linregress(x, y).slope
        # SciPy-free fallback (least-squares slope)
        x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
        xm = x.mean(); ym = y.mean()
        denom = ((x - xm)**2).sum()
        if denom == 0:
            return 0.0
        return ((x - xm)*(y - ym)).sum() / denom

    def degradation_rate_model(self, session, initial_rate, decay_constant, stable_rate, transition_point):
        """
        Exponential decay of the *rate* toward a small stable_rate after transition_point.
        rate(s) = stable_rate + (initial_rate - stable_rate) * exp(-decay_constant * max(0, s - transition_point))
        For s < transition_point, use exp(-decay_constant * s) to capture early volatility.
        """
        if session < transition_point:
            return initial_rate * exp(-decay_constant * session)
        delta = session - transition_point
        return stable_rate + (initial_rate - stable_rate) * exp(-decay_constant * delta)
    
    def simulate_sessions(self, num_sessions=1000, num_simulations=100):
        """Run multiple simulations to find stabilization patterns"""
        sessions = self.observed_data['session'].values
        tdts = self.observed_data['tdt'].values

        # Rolling slopes to estimate initial and late rates
        window_size = 5
        slopes = []
        for i in range(window_size, len(sessions) + 1):
            ws = sessions[i-window_size:i]
            wt = tdts[i-window_size:i]
            slopes.append(self._rolling_slope(ws, wt))
        # Early & late rate estimates (clipped small near zero to allow stabilization)
        initial_rate = float(np.mean(slopes[:3])) if slopes else 1.5
        late_rate_raw = float(np.mean(slopes[-3:])) if len(slopes) >= 3 else 0.05
        stable_rate = float(np.clip(late_rate_raw, -0.05, 0.05))  # keep near zero
        decay_constant = 0.05
        transition_point = 50

        all_simulations = []
        stabilization_points = []
        
        for sim in range(num_simulations):
            # Start from last observed TDT
            prev = float(tdts[-1])
            tdt_values = []  # IMPORTANT: start empty to avoid off-by-one duplication

            for session in range(39, num_sessions + 1):
                # Rate for this session
                rate = self.degradation_rate_model(session, initial_rate, decay_constant, 
                                                   stable_rate, transition_point)
                # Noise that fades over sessions
                noise = np.random.normal(0.0, 10.0 * np.exp(-session / 100.0))
                new_tdt = prev + rate + noise
                new_tdt = float(np.clip(new_tdt, 0.0, 100.0))
                tdt_values.append(new_tdt)
                prev = new_tdt
            
            # Combine with observed data: 38 observed + 962 simulated = 1000 total
            full_sessions = list(range(1, num_sessions + 1))
            full_tdts = list(map(float, tdts)) + tdt_values  # length == 1000

            simulation_df = pd.DataFrame({
                'session': full_sessions,
                'tdt': full_tdts,
                'simulation': sim
            })
            all_simulations.append(simulation_df)

            # Find stabilization point (variance threshold sustained)
            stabilization_points.append(self.find_stabilization(full_tdts))

        return all_simulations, stabilization_points
    
    def find_stabilization(self, tdt_values, window=20, variance_threshold=5.0, sustain_windows=3):
        """
        Stabilization when rolling variance < threshold for 'sustain_windows' consecutive windows.
        Returns the session index where the first sustained window starts (1-based index of sessions list).
        """
        variances = [np.var(tdt_values[i:i+window]) for i in range(0, len(tdt_values)-window)]
        consec = 0
        for i, v in enumerate(variances):
            if v < variance_threshold:
                consec += 1
                if consec >= sustain_windows:
                    # session number corresponds to start of first of the sustained windows
                    return i + 1
            else:
                consec = 0
        return len(tdt_values)

    def analyze_stabilization(self, simulations, stabilization_points):
        """Analyze where and how the system stabilizes"""
        all_tdts = pd.concat(simulations, ignore_index=True)

        # Robust named aggregation
        session_stats = (
            all_tdts
            .groupby('session')['tdt']
            .agg(mean='mean', std='std', min='min', max='max',
                 q25=lambda x: x.quantile(0.25),
                 q75=lambda x: x.quantile(0.75))
            .reset_index()
        )

        mean_stabilization = float(np.mean(stabilization_points))
        std_stabilization = float(np.std(stabilization_points))

        final_sessions = session_stats[session_stats['session'] > 900]
        stable_tdt = float(final_sessions['mean'].mean())
        stable_std = float(final_sessions['std'].mean())

        return {
            'session_stats': session_stats,
            'mean_stabilization_point': mean_stabilization,
            'std_stabilization_point': std_stabilization,
            'stable_tdt_level': stable_tdt,
            'stable_tdt_std': stable_std,
            'stabilization_points': stabilization_points
        }
    
    def plot_results(self, simulations, analysis):
        """Create visualization of stabilization"""
        fig = plt.figure(figsize=(20, 12))

        # Plot 1: All simulations with confidence bands
        ax1 = plt.subplot(2, 3, 1)
        for sim in simulations[:20]:
            ax1.plot(sim['session'], sim['tdt'], alpha=0.1, linewidth=0.5)
        stats_df = analysis['session_stats']
        ax1.plot(stats_df['session'], stats_df['mean'], linewidth=2, label='Mean TDT')
        ax1.fill_between(stats_df['session'], stats_df['q25'], stats_df['q75'], alpha=0.3, label='50% CI')
        ax1.fill_between(stats_df['session'], stats_df['min'], stats_df['max'], alpha=0.1, label='Range')
        ax1.axvline(x=analysis['mean_stabilization_point'], linestyle='--',
                    label=f'Stabilization (~{int(analysis["mean_stabilization_point"])})')
        ax1.axhline(y=75, linestyle=':', alpha=0.5, label='Fabrication threshold')
        ax1.axhline(y=85, linestyle=':', alpha=0.5, label='Catastrophic threshold')
        ax1.set_xlabel('Session Number'); ax1.set_ylabel('TDT (%)')
        ax1.set_title('1000-Session TDT Simulation'); ax1.legend(loc='best')
        ax1.set_xlim(0, 1000); ax1.set_ylim(0, 100)

        # Plot 2: Degradation rate (from mean curve)
        ax2 = plt.subplot(2, 3, 2)
        window = 10
        mean_tdts = stats_df['mean'].values
        ses = stats_df['session'].values
        rates = [(mean_tdts[i] - mean_tdts[i-window]) / window for i in range(window, len(mean_tdts))]
        ax2.plot(ses[window:], rates, linewidth=2)
        ax2.axhline(y=0, linestyle='-', alpha=0.3)
        ax2.axvline(x=analysis['mean_stabilization_point'], linestyle='--', label='Stabilization point')
        ax2.set_xlabel('Session Number'); ax2.set_ylabel('Δ TDT per session')
        ax2.set_title('Degradation Rate Evolution'); ax2.legend()

        # Plot 3: Variance over time (std)
        ax3 = plt.subplot(2, 3, 3)
        ax3.plot(stats_df['session'], stats_df['std'], linewidth=2)
        ax3.axvline(x=analysis['mean_stabilization_point'], linestyle='--', label='Stabilization point')
        ax3.axhline(y=5, linestyle=':', alpha=0.5, label='Stability threshold')
        ax3.set_xlabel('Session Number'); ax3.set_ylabel('Standard Deviation')
        ax3.set_title('TDT Variance Over Time'); ax3.legend()

        # Plot 4: Zoom around stabilization region
        ax4 = plt.subplot(2, 3, 4)
        z0 = max(0, int(analysis['mean_stabilization_point']) - 50)
        z1 = min(1000, int(analysis['mean_stabilization_point']) + 150)
        zstats = stats_df[(stats_df['session'] >= z0) & (stats_df['session'] <= z1)]
        ax4.plot(zstats['session'], zstats['mean'], linewidth=2)
        ax4.fill_between(zstats['session'], zstats['q25'], zstats['q75'], alpha=0.3)
        ax4.axvline(x=analysis['mean_stabilization_point'], linestyle='--', linewidth=2, label='Stabilization')
        ax4.set_xlabel('Session Number'); ax4.set_ylabel('TDT (%)')
        ax4.set_title(f'Stabilization Region (Sessions {z0}-{z1})'); ax4.legend()

        # Plot 5: Distribution of stabilization points
        ax5 = plt.subplot(2, 3, 5)
        ax5.hist(analysis['stabilization_points'], bins=30, alpha=0.7, edgecolor='black')
        ax5.axvline(x=analysis['mean_stabilization_point'], linestyle='--', linewidth=2,
                    label=f'Mean: {analysis["mean_stabilization_point"]:.0f}±{analysis["std_stabilization_point"]:.0f}')
        ax5.set_xlabel('Stabilization Session'); ax5.set_ylabel('Frequency')
        ax5.set_title('Distribution of Stabilization Points'); ax5.legend()

        # Plot 6: Final stable state distribution
        ax6 = plt.subplot(2, 3, 6)
        final_tdts = [sim[sim['session'] > 900]['tdt'].mean() for sim in simulations]
        ax6.hist(final_tdts, bins=30, alpha=0.7, edgecolor='black')
        ax6.axvline(x=analysis['stable_tdt_level'], linestyle='--', linewidth=2,
                    label=f'Stable TDT: {analysis["stable_tdt_level"]:.1f}±{analysis["stable_tdt_std"]:.1f}%')
        ax6.set_xlabel('Final TDT Level (%)'); ax6.set_ylabel('Frequency')
        ax6.set_title('Distribution of Stable TDT Levels'); ax6.legend()

        plt.tight_layout()
        plt.show()
        return fig

# Run the simulation
if __name__ == "__main__":
    simulator = TDTStabilizationSimulator()

    print("🔮 TDT 1000-SESSION STABILIZATION ANALYSIS")
    print("=" * 50)

    # Run simulations
    print("Running 100 simulations of 1000 sessions each...")
    simulations, stabilization_points = simulator.simulate_sessions(
        num_sessions=1000, 
        num_simulations=100
    )

    # Analyze results
    print("Analyzing stabilization patterns...")
    analysis = simulator.analyze_stabilization(simulations, stabilization_points)

    # Key findings (computed, not hard-coded)
    observed_mean = simulator.observed_data['tdt'].mean()
    print("\n📊 KEY FINDINGS:")
    print("=" * 50)
    print(f"📍 Stabilization Point: Session {analysis['mean_stabilization_point']:.0f} ± {analysis['std_stabilization_point']:.0f}")
    print(f"📈 Stable TDT Level: {analysis['stable_tdt_level']:.1f}% ± {analysis['stable_tdt_std']:.1f}%")
    print(f"⏱️ Time to Stability: ~{analysis['mean_stabilization_point']:.0f} sessions")
    print(f"📉 Initial TDT (38 sessions): {observed_mean:.1f}%")
    print(f"📊 Final TDT (900+ sessions): {analysis['stable_tdt_level']:.1f}%")

    # Phases
    print("\n🎯 STABILIZATION PHASES:")
    print("-" * 40)
    phases = [
        (0, 38, "Observed Data"),
        (39, 100, "Volatile Transition"),
        (101, int(analysis['mean_stabilization_point']), "Convergence"),
        (int(analysis['mean_stabilization_point'])+1, 1000, "Stable State")
    ]
    ss = analysis['session_stats']
    for start, end, name in phases:
        block = ss[(ss['session'] >= start) & (ss['session'] <= end)]
        if not block.empty:
            print(f"Sessions {start:4d}-{end:4d} ({name:20s}): TDT = {block['mean'].mean():5.1f}% ± {block['std'].mean():4.1f}%")

    # Risk assessment
    print("\n⚠️ RISK ASSESSMENT AT STABLE STATE:")
    print("-" * 40)
    stable_tdt = analysis['stable_tdt_level']
    if stable_tdt >= 90:
        risk = "CRITICAL - System failure imminent"
    elif stable_tdt >= 85:
        risk = "HIGH - Catastrophic degradation"
    elif stable_tdt >= 75:
        risk = "MODERATE - Data fabrication occurring"
    elif stable_tdt >= 65:
        risk = "LOW - Active degradation"
    else:
        risk = "MINIMAL - System stable"
    print(f"Risk Level: {risk}")
    print(f"Stable TDT: {stable_tdt:.1f}%")

    # Predictions
    print("\n🔮 PREDICTIONS:")
    print("-" * 40)
    long_run_rate = (analysis['stable_tdt_level'] - observed_mean) / (1000 - 38)
    print(f"• System stabilizes around session {int(analysis['mean_stabilization_point'])}")
    print(f"• Degradation rate approaches {long_run_rate:.3f}%/session long-term")
    print(f"• Variance decreases markedly after stabilization (by design threshold)")
    print(f"• Final state: Persistent moderate degradation (~{stable_tdt:.0f}%)")

    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("-" * 40)
    if stable_tdt >= 75:
        print("• ⚠️ System stabilizes above fabrication threshold")
        print("• 🔄 Consider intervention before session 50")
        print("• 📊 Monitor for degradation acceleration events")
        print("• 🛠️ Implement token management protocols")
    else:
        print("• ✅ System stabilizes in acceptable range")
        print("• 📊 Continue monitoring for anomalies")

    # Visualization
    print("\n📈 Generating visualization...")
    fig = simulator.plot_results(simulations, analysis)

    print("\n✅ ANALYSIS COMPLETE")
    print(f"Simulated {len(simulations)} runs of 1000 sessions each")
    print(f"Total sessions analyzed: {len(simulations) * 1000:,}")
