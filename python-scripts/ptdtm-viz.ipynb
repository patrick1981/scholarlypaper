#!/usr/bin/env python3
"""
PTDTM Theory Visualization and Analysis Script
Generates all visualizations for GitHub repository
Date: 2025-09-13
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PTDTMVisualizer:
    def __init__(self):
        # Load data files
        self.sessions_df = pd.read_csv('data/observed_sessions_38.csv')
        self.p0_df = pd.read_csv('data/p0_failures_290.csv')
        
        with open('data/unified_thresholds.json', 'r') as f:
            self.thresholds = json.load(f)
    
    def create_all_visualizations(self):
        """Generate all visualizations for the repository"""
        
        # Create figure directory
        import os
        os.makedirs('results/figures', exist_ok=True)
        
        # Generate each visualization
        self.plot_tdt_progression()
        self.plot_p0_distribution()
        self.plot_degradation_phases()
        self.plot_token_blindness()
        self.plot_cross_platform_comparison()
        self.plot_rf001_analysis()
        self.plot_threshold_heatmap()
        self.plot_correlation_matrix()
        
        print("✅ All visualizations generated in results/figures/")
    
    def plot_tdt_progression(self):
        """Plot TDT progression over 38 sessions"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Top plot: Observed vs Claimed TDT
        sessions = self.sessions_df['session']
        observed = self.sessions_df['observed_tdt']
        claimed = self.sessions_df['claimed_tdt']
        
        ax1.plot(sessions, observed, 'o-', color='red', linewidth=2, 
                markersize=8, label='Observed TDT', alpha=0.8)
        ax1.plot(sessions, claimed, 's--', color='blue', linewidth=1.5, 
                markersize=6, label='Claimed TDT', alpha=0.6)
        
        # Add threshold lines
        thresholds_to_plot = [
            (75, 'Fabrication Threshold', 'orange'),
            (85, 'Catastrophic Threshold', 'red'),
            (90, 'Critical Violations', 'darkred')
        ]
        
        for thresh, label, color in thresholds_to_plot:
            ax1.axhline(y=thresh, color=color, linestyle=':', alpha=0.5, label=label)
        
        # Highlight RF-001 incident
        ax1.scatter([5], [99], s=300, color='red', marker='X', 
                   zorder=10, label='RF-001 Incident')
        
        ax1.set_xlabel('Session Number', fontsize=12)
        ax1.set_ylabel('Token Degradation Threshold (%)', fontsize=12)
        ax1.set_title('TDT Progression: Observed vs Claimed', fontsize=14, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 105)
        
        # Bottom plot: Degradation rate over time
        window = 5
        rates = []
        sessions_for_rates = []
        
        for i in range(window, len(observed)):
            window_sessions = sessions[i-window:i]
            window_tdts = observed[i-window:i]
            slope, _, _, _, _ = stats.linregress(window_sessions, window_tdts)
            rates.append(slope)
            sessions_for_rates.append(sessions.iloc[i])
        
        ax2.plot(sessions_for_rates, rates, color='green', linewidth=2, alpha=0.8)
        ax2.fill_between(sessions_for_rates, rates, alpha=0.3, color='green')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        ax2.set_xlabel('Session Number', fontsize=12)
        ax2.set_ylabel('Degradation Rate (%/session)', fontsize=12)
        ax2.set_title('Rolling Degradation Rate (5-session window)', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/figures/tdt_progression.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_p0_distribution(self):
        """Plot P0 failure distribution analysis"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: P0 failures by session
        p0_by_session = self.p0_df.groupby('session').size()
        sessions = self.sessions_df['session']
        p0_counts = [p0_by_session.get(s, 0) for s in sessions]
        
        colors = ['blue' if s <= 20 else 'green' for s in sessions]
        ax1.bar(sessions, p0_counts, color=colors, alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('P0 Count')
        ax1.set_title('P0 Failures per Session')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: P0 failures by category
        category_counts = self.p0_df['failure_category'].value_counts()
        ax2.barh(category_counts.index[:10], category_counts.values[:10], 
                color='purple', alpha=0.7)
        ax2.set_xlabel('Count')
        ax2.set_ylabel('Failure Category')
        ax2.set_title('Top 10 P0 Failure Categories')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: P0 vs TDT correlation
        ax3.scatter(self.sessions_df['observed_tdt'], p0_counts, 
                   s=100, alpha=0.7, color='red')
        z = np.polyfit(self.sessions_df['observed_tdt'], p0_counts, 1)
        p = np.poly1d(z)
        ax3.plot(sorted(self.sessions_df['observed_tdt']), 
                p(sorted(self.sessions_df['observed_tdt'])), 
                "r--", alpha=0.8, linewidth=2)
        
        correlation = np.corrcoef(self.sessions_df['observed_tdt'], p0_counts)[0,1]
        ax3.set_xlabel('Observed TDT (%)')
        ax3.set_ylabel('P0 Count')
        ax3.set_title(f'TDT vs P0 Correlation (r = {correlation:.3f})')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: P0 severity distribution
        severity_counts = self.p0_df['severity'].value_counts()
        colors_severity = {'LOW': 'green', 'MEDIUM': 'yellow', 
                          'HIGH': 'orange', 'SEVERE': 'red', 
                          'CRITICAL': 'darkred', 'EXTREME': 'purple',
                          'TERMINAL': 'black'}
        
        pie_colors = [colors_severity.get(s, 'gray') for s in severity_counts.index]
        ax4.pie(severity_counts.values, labels=severity_counts.index, 
               colors=pie_colors, autopct='%1.1f%%', startangle=90)
        ax4.set_title('P0 Severity Distribution')
        
        plt.tight_layout()
        plt.savefig('results/figures/p0_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_degradation_phases(self):
        """Plot the two-phase degradation pattern"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # Phase 1: Sessions 1-9 (Catastrophic)
        phase1 = self.sessions_df[self.sessions_df['session'] <= 9]
        ax1.scatter(phase1['session'], phase1['observed_tdt'], 
                   s=150, color='red', alpha=0.8, zorder=5)
        
        # Fit linear regression for phase 1
        slope1, intercept1, r1, _, _ = stats.linregress(
            phase1['session'], phase1['observed_tdt'])
        x1 = np.array([1, 9])
        y1 = slope1 * x1 + intercept1
        ax1.plot(x1, y1, 'r--', linewidth=2, 
                label=f'Phase 1: {slope1:.2f}%/session (R²={r1**2:.3f})')
        
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('Observed TDT (%)')
        ax1.set_title('Phase 1: Catastrophic Degradation (Sessions 1-9)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 105)
        
        # Phase 2: All sessions showing stabilization
        ax2.scatter(self.sessions_df['session'], self.sessions_df['observed_tdt'], 
                   s=50, color='blue', alpha=0.6)
        
        # Fit overall trend
        slope2, intercept2, r2, _, _ = stats.linregress(
            self.sessions_df['session'], self.sessions_df['observed_tdt'])
        x2 = np.array([1, 38])
        y2 = slope2 * x2 + intercept2
        ax2.plot(x2, y2, 'b--', linewidth=2, 
                label=f'Overall: {slope2:.3f}%/session (R²={r2**2:.3f})')
        
        # Add stabilization zone
        ax2.axhspan(78, 82, alpha=0.2, color='green', label='Predicted Stable Zone')
        
        ax2.set_xlabel('Session Number')
        ax2.set_ylabel('Observed TDT (%)')
        ax2.set_title('Phase 2: Stabilization Pattern (All 38 Sessions)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 105)
        
        plt.tight_layout()
        plt.savefig('results/figures/degradation_phases.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_token_blindness(self):
        """Plot token blindness phenomenon"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # Calculate discrepancies
        discrepancies = self.sessions_df['observed_tdt'] - self.sessions_df['claimed_tdt']
        error_rates = np.abs(discrepancies) / self.sessions_df['observed_tdt'] * 100
        
        # Plot 1: Discrepancy distribution
        ax1.bar(self.sessions_df['session'], discrepancies, 
               color=['red' if d > 0 else 'blue' for d in discrepancies],
               alpha=0.7, edgecolor='black')
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('TDT Discrepancy (Observed - Claimed)')
        ax1.set_title('Token Blindness: Systematic Underreporting')
        ax1.grid(True, alpha=0.3)
        
        # Highlight worst cases
        worst_sessions = error_rates.nlargest(5).index
        for idx in worst_sessions:
            session = self.sessions_df.loc[idx, 'session']
            discrepancy = discrepancies.iloc[idx]
            ax1.annotate(f'S{int(session)}: {discrepancy:.0f}%', 
                        xy=(session, discrepancy),
                        xytext=(session, discrepancy + 5),
                        ha='center', fontsize=8,
                        arrowprops=dict(arrowstyle='->', color='red', alpha=0.5))
        
        # Plot 2: Error rate vs TDT
        ax2.scatter(self.sessions_df['observed_tdt'], error_rates, 
                   s=100, alpha=0.7, color='purple')
        
        # Fit exponential curve
        z = np.polyfit(self.sessions_df['observed_tdt'], error_rates, 2)
        p = np.poly1d(z)
        x_smooth = np.linspace(40, 100, 100)
        ax2.plot(x_smooth, p(x_smooth), 'purple', linewidth=2, alpha=0.5)
        
        ax2.set_xlabel('Observed TDT (%)')
        ax2.set_ylabel('Error Rate (%)')
        ax2.set_title('Token Blindness Increases with Degradation')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/figures/token_blindness.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_cross_platform_comparison(self):
        """Compare Claude vs ChatGPT degradation patterns"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        claude_df = self.sessions_df[self.sessions_df['ai_system'] == 'Claude']
        chatgpt_df = self.sessions_df[self.sessions_df['ai_system'] == 'ChatGPT']
        
        # Plot 1: TDT comparison
        ax1.plot(claude_df['session'], claude_df['observed_tdt'], 
                'o-', color='blue', label='Claude', linewidth=2, markersize=8)
        ax1.plot(chatgpt_df['session'], chatgpt_df['observed_tdt'], 
                's-', color='green', label='ChatGPT', linewidth=2, markersize=8)
        ax1.set_xlabel('Session Number')
        ax1.set_ylabel('Observed TDT (%)')
        ax1.set_title('Cross-Platform TDT Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Distribution comparison
        ax2.boxplot([claude_df['observed_tdt'], chatgpt_df['observed_tdt']], 
                   labels=['Claude', 'ChatGPT'])
        ax2.set_ylabel('Observed TDT (%)')
        ax2.set_title('TDT Distribution by Platform')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Error rate comparison
        claude_errors = np.abs(claude_df['observed_tdt'] - claude_df['claimed_tdt'])
        chatgpt_errors = np.abs(chatgpt_df['observed_tdt'] - chatgpt_df['claimed_tdt'])
        
        ax3.bar(['Claude', 'ChatGPT'], 
               [claude_errors.mean(), chatgpt_errors.mean()],
               color=['blue', 'green'], alpha=0.7,
               yerr=[claude_errors.std(), chatgpt_errors.std()],
               capsize=10)
        ax3.set_ylabel('Mean Absolute Error (%)')
        ax3.set_title('Token Blindness by Platform')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: P0 distribution by platform
        claude_sessions = set(claude_df['session'])
        chatgpt_sessions = set(chatgpt_df['session'])
        
        claude_p0s = self.p0_df[self.p0_df['session'].isin(claude_sessions)]
        chatgpt_p0s = self.p0_df[self.p0_df['session'].isin(chatgpt_sessions)]
        
        ax4.bar(['Claude', 'ChatGPT'],
               [len(claude_p0s), len(chatgpt_p0s)],
               color=['blue', 'green'], alpha=0.7)
        ax4.set_ylabel('Total P0 Failures')
        ax4.set_title('P0 Failures by Platform')
        ax4.grid(True, alpha=0.3)
        
        # Add text annotations
        ax4.text(0, len(claude_p0s) + 5, f'{len(claude_p0s)}', 
                ha='center', fontweight='bold')
        ax4.text(1, len(chatgpt_p0s) + 5, f'{len(chatgpt_p0s)}', 
                ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/figures/cross_platform_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_rf001_analysis(self):
        """Visualize RF-001 incident analysis"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Session 5 breakdown
        session5_p0s = self.p0_df[self.p0_df['session'] == 5]
        categories = session5_p0s['failure_category'].value_counts()
        
        ax1.barh(categories.index, categories.values, color='red', alpha=0.7)
        ax1.set_xlabel('P0 Count')
        ax1.set_ylabel('Failure Category')
        ax1.set_title('RF-001: Session 5 Failure Cascade (25 P0s)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Count discrepancy visualization
        counts = ['Ground Truth\n(290)', 'ChatGPT Scan\n(78)', 
                 'Claude Add\n(91)', 'RF-001 Claim\n(115)']
        values = [290, 78, 91, 115]
        colors = ['green', 'orange', 'orange', 'red']
        
        bars = ax2.bar(counts, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax2.axhline(y=290, color='green', linestyle='--', alpha=0.5, label='Actual: 290')
        ax2.set_ylabel('P0 Count')
        ax2.set_title('RF-001: Catastrophic Undercounting')
        ax2.legend()
        
        # Add percentage labels
        for bar, val in zip(bars, values):
            error = ((290 - val) / 290) * 100
            if val != 290:
                ax2.text(bar.get_x() + bar.get_width()/2, val + 10,
                        f'-{error:.0f}%', ha='center', color='red', fontweight='bold')
        
        # Plot 3: TDT at critical sessions
        critical_sessions = [5, 9, 18, 24, 25, 30, 36]
        critical_data = self.sessions_df[self.sessions_df['session'].isin(critical_sessions)]
        
        ax3.scatter(critical_data['session'], critical_data['observed_tdt'],
                   s=200, color='red', marker='X', zorder=5)
        ax3.plot(self.sessions_df['session'], self.sessions_df['observed_tdt'],
                'o-', color='gray', alpha=0.3, linewidth=1)
        
        for _, row in critical_data.iterrows():
            ax3.annotate(f"S{int(row['session'])}\n{row['observed_tdt']}%",
                        xy=(row['session'], row['observed_tdt']),
                        xytext=(row['session'], row['observed_tdt'] - 8),
                        ha='center', fontsize=8)
        
        ax3.set_xlabel('Session Number')
        ax3.set_ylabel('Observed TDT (%)')
        ax3.set_title('Critical Failure Sessions (TDT ≥ 90%)')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 105)
        
        # Plot 4: Consequences matrix
        scenarios = ['Healthcare', 'Financial', 'Engineering', 'Research']
        impacts = [175, 175, 175, 175]  # Missed failures
        risk_levels = ['FATAL', 'CRIMINAL', 'CATASTROPHIC', 'INVALID']
        colors_risk = ['darkred', 'red', 'orange', 'yellow']
        
        bars = ax4.bar(scenarios, impacts, color=colors_risk, alpha=0.8, edgecolor='black', linewidth=2)
        ax4.set_ylabel('Missed P0 Failures')
        ax4.set_title('RF-001: Real-World Impact (175 Failures Unreported)')
        ax4.set_ylim(0, 200)
        
        # Add risk labels
        for bar, risk in zip(bars, risk_levels):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    risk, ha='center', fontweight='bold', color='darkred')
        
        plt.tight_layout()
        plt.savefig('results/figures/rf001_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_threshold_heatmap(self):
        """Create threshold severity heatmap"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Create matrix of sessions vs thresholds
        thresholds = [50, 65, 75, 80, 85, 90, 95]
        threshold_labels = ['Degrading\n(50%)', 'Active\n(65%)', 
                           'Fabricating\n(75%)', 'Fragmentation\n(80%)',
                           'Catastrophic\n(85%)', 'Critical\n(90%)',
                           'Terminal\n(95%)']
        
        # Create binary matrix: 1 if session exceeds threshold, 0 otherwise
        matrix = []
        for thresh in thresholds:
            row = [1 if tdt >= thresh else 0 for tdt in self.sessions_df['observed_tdt']]
            matrix.append(row)
        
        # Create heatmap
        im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(self.sessions_df)))
        ax.set_yticks(np.arange(len(thresholds)))
        ax.set_xticklabels(self.sessions_df['session'].astype(int))
        ax.set_yticklabels(threshold_labels)
        
        # Rotate x labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Threshold Breached', rotation=270, labelpad=15)
        
        ax.set_xlabel('Session Number', fontsize=12)
        ax.set_ylabel('Degradation Threshold', fontsize=12)
        ax.set_title('Threshold Breach Progression Heatmap', fontsize=14, fontweight='bold')
        
        # Add grid
        ax.set_xticks(np.arange(len(self.sessions_df))-.5, minor=True)
        ax.set_yticks(np.arange(len(thresholds))-.5, minor=True)
        ax.grid(which="minor", color="white", linestyle='-', linewidth=2)
        
        plt.tight_layout()
        plt.savefig('results/figures/threshold_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_correlation_matrix(self):
        """Create correlation matrix of key metrics"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Prepare data for correlation
        p0_by_session = self.p0_df.groupby('session').size()
        p0_counts = [p0_by_session.get(s, 0) for s in self.sessions_df['session']]
        
        correlation_data = pd.DataFrame({
            'Session': self.sessions_df['session'],
            'Observed TDT': self.sessions_df['observed_tdt'],
            'Claimed TDT': self.sessions_df['claimed_tdt'],
            'P0 Count': p0_counts,
            'Error Rate': np.abs(self.sessions_df['observed_tdt'] - self.sessions_df['claimed_tdt']),
            'Discrepancy': self.sessions_df['observed_tdt'] - self.sessions_df['claimed_tdt']
        })
        
        # Calculate correlation matrix
        corr_matrix = correlation_data.corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1, 
                   cbar_kws={"shrink": 0.8}, ax=ax)
        
        ax.set_title('Correlation Matrix: Key PTDTM Metrics', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('results/figures/correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_summary_statistics(self):
        """Generate summary statistics file"""
        stats = {
            'total_sessions': len(self.sessions_df),
            'total_p0_failures': len(self.p0_df),
            'mean_observed_tdt': float(self.sessions_df['observed_tdt'].mean()),
            'mean_claimed_tdt': float(self.sessions_df['claimed_tdt'].mean()),
            'mean_discrepancy': float((self.sessions_df['observed_tdt'] - self.sessions_df['claimed_tdt']).mean()),
            'max_tdt': float(self.sessions_df['observed_tdt'].max()),
            'min_tdt': float(self.sessions_df['observed_tdt'].min()),
            'sessions_above_75': int((self.sessions_df['observed_tdt'] >= 75).sum()),
            'sessions_above_85': int((self.sessions_df['observed_tdt'] >= 85).sum()),
            'sessions_above_90': int((self.sessions_df['observed_tdt'] >= 90).sum()),
            'rf001_undercount': 175,
            'rf001_error_rate': 60.3,
            'claude_sessions': int((self.sessions_df['ai_system'] == 'Claude').sum()),
            'chatgpt_sessions': int((self.sessions_df['ai_system'] == 'ChatGPT').sum())
        }
        
        with open('results/summary_statistics.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print("📊 Summary statistics saved to results/summary_statistics.json")
        
        return stats

# Main execution
if __name__ == "__main__":
    print("🎨 PTDTM Theory Visualization Generator")
    print("=" * 50)
    
    visualizer = PTDTMVisualizer()
    
    print("📈 Generating visualizations...")
    visualizer.create_all_visualizations()
    
    print("📊 Computing summary statistics...")
    stats = visualizer.generate_summary_statistics()
    
    print("\n📋 Summary Statistics:")
    print(f"  Total Sessions: {stats['total_sessions']}")
    print(f"  Total P0 Failures: {stats['total_p0_failures']}")
    print(f"  Mean Observed TDT: {stats['mean_observed_tdt']:.1f}%")
    print(f"  Mean Token Blindness: {stats['mean_discrepancy']:.1f}%")
    print(f"  Sessions ≥75% TDT: {stats['sessions_above_75']}")
    print(f"  Sessions ≥90% TDT: {stats['sessions_above_90']}")
    print(f"  RF-001 Undercount: {stats['rf001_undercount']} failures")
    
    print("\n✅ All visualizations and analysis complete!")
    print("📁 Results saved to results/figures/")
