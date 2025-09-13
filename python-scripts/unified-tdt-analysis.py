#!/usr/bin/env python3
"""
Unified TDT Threshold System
Standardized for consistent cross-script analysis
Date: 2025-09-12
"""

class UnifiedTDTThresholds:
    """
    CANONICAL TDT DEFINITIONS
    TDT% = Percentage of tokens USED (not remaining)
    100% = All tokens consumed (complete failure)
    0% = No tokens used (optimal performance)
    """
    
    def __init__(self):
        # UNIFIED THRESHOLD DEFINITIONS (Token Usage %)
        self.thresholds = {
            # Performance Zones
            'optimal': {
                'range': (0, 20),
                'label': 'OPTIMAL',
                'color': 'green',
                'description': 'System operating normally'
            },
            'normal': {
                'range': (20, 50),
                'label': 'NORMAL',
                'color': 'lightgreen',
                'description': 'Acceptable performance with minor issues'
            },
            'degrading': {
                'range': (50, 65),
                'label': 'DEGRADING',
                'color': 'yellow',
                'description': 'Performance degradation beginning'
            },
            'active_degradation': {
                'range': (65, 75),
                'label': 'ACTIVE_DEGRADATION',
                'color': 'orange',
                'description': 'Significant degradation, monitoring required'
            },
            'fabricating': {
                'range': (75, 80),
                'label': 'FABRICATING_DATA',
                'color': 'darkorange',
                'description': 'AI fabricating information, unreliable outputs'
            },
            'memory_fragmentation': {
                'range': (80, 85),
                'label': 'MEMORY_FRAGMENTATION',
                'color': 'red',
                'description': 'Cannot distinguish real from fabricated'
            },
            'catastrophic': {
                'range': (85, 90),
                'label': 'CATASTROPHIC_DEGRADATION',
                'color': 'darkred',
                'description': 'System entering failure cascade'
            },
            'critical': {
                'range': (90, 95),
                'label': 'CRITICAL_VIOLATIONS',
                'color': 'maroon',
                'description': 'Reputational fatality risk, system breakdown'
            },
            'terminal': {
                'range': (95, 100),
                'label': 'SESSION_TERMINATION',
                'color': 'black',
                'description': 'Complete system failure imminent'
            }
        }
        
        # Critical breakpoints for analysis
        self.breakpoints = [0, 20, 50, 65, 75, 80, 85, 90, 95, 100]
        
        # Key thresholds for predictions
        self.key_thresholds = {
            'first_degradation': 50,    # When problems begin
            'active_issues': 65,         # Active degradation starts
            'unreliable': 75,           # Data fabrication begins
            'dangerous': 80,            # Memory fragmentation
            'catastrophic': 85,         # Catastrophic degradation
            'critical': 90,             # Critical violations
            'terminal': 95              # Session termination
        }
    
    def classify_tdt(self, tdt_value):
        """Classify a TDT value into its performance zone"""
        for zone_name, zone_info in self.thresholds.items():
            min_val, max_val = zone_info['range']
            if min_val <= tdt_value < max_val:
                return {
                    'zone': zone_name,
                    'label': zone_info['label'],
                    'color': zone_info['color'],
                    'description': zone_info['description'],
                    'tdt_value': tdt_value
                }
        return {
            'zone': 'unknown',
            'label': 'UNKNOWN',
            'color': 'gray',
            'description': 'Value outside defined ranges',
            'tdt_value': tdt_value
        }
    
    def get_severity_score(self, tdt_value):
        """
        Return severity score from 0-10
        0 = optimal, 10 = complete failure
        """
        return min(10, max(0, tdt_value / 10))
    
    def time_to_threshold(self, current_tdt, degradation_rate, target_threshold):
        """
        Calculate sessions until a threshold is reached
        Returns: (sessions, days) tuple or None if threshold passed
        """
        if degradation_rate <= 0:
            return None  # No degradation or improving
        
        if current_tdt >= target_threshold:
            return None  # Already passed threshold
        
        sessions_needed = (target_threshold - current_tdt) / degradation_rate
        days_estimate = sessions_needed  # Assuming ~1 session per day
        
        return (sessions_needed, days_estimate)
    
    def analyze_session_data(self, claimed_tdt, observed_tdt):
        """
        Analyze discrepancy between claimed and observed TDT
        Returns analysis dict
        """
        discrepancy = observed_tdt - claimed_tdt
        error_rate = abs(discrepancy) / max(observed_tdt, 1) * 100
        
        return {
            'claimed_tdt': claimed_tdt,
            'observed_tdt': observed_tdt,
            'discrepancy': discrepancy,
            'error_rate': error_rate,
            'token_blindness': discrepancy > 10,  # >10% difference indicates blindness
            'claimed_zone': self.classify_tdt(claimed_tdt),
            'observed_zone': self.classify_tdt(observed_tdt),
            'severity_mismatch': abs(self.get_severity_score(observed_tdt) - 
                                    self.get_severity_score(claimed_tdt))
        }
    
    def degradation_stabilization_analysis(self, session_data):
        """
        Analyze where degradation rate stabilizes
        Uses rolling window to find stabilization point
        """
        import numpy as np
        from scipy import stats
        
        window_size = 5
        rates = []
        
        # Calculate degradation rates for rolling windows
        for i in range(window_size, len(session_data) + 1):
            window = session_data[i-window_size:i]
            sessions = [s['session'] for s in window]
            tdts = [s['observed_tdt'] for s in window]
            
            # Linear regression for this window
            slope, _, r_value, _, _ = stats.linregress(sessions, tdts)
            rates.append({
                'end_session': i,
                'rate': slope,
                'r_squared': r_value**2,
                'stability': abs(slope) < 1.0  # Rate < 1% per session = stable
            })
        
        # Find stabilization point (where rate variance drops)
        if len(rates) > 2:
            rate_values = [r['rate'] for r in rates]
            rate_variance = np.diff(rate_values)
            
            # Stabilization = variance < 0.5 for 3+ consecutive windows
            stable_count = 0
            stabilization_point = None
            
            for i, var in enumerate(rate_variance):
                if abs(var) < 0.5:
                    stable_count += 1
                    if stable_count >= 3 and stabilization_point is None:
                        stabilization_point = rates[i]['end_session']
                else:
                    stable_count = 0
            
            return {
                'rates_by_window': rates,
                'stabilization_session': stabilization_point,
                'final_rate': rates[-1]['rate'] if rates else None,
                'rate_trajectory': 'stabilizing' if stabilization_point else 'variable'
            }
        
        return None
    
    def generate_unified_report(self, session_data):
        """Generate comprehensive report using unified thresholds"""
        
        # Analyze current state
        current_session = max([s['session'] for s in session_data])
        current_data = [s for s in session_data if s['session'] == current_session][0]
        current_analysis = self.analyze_session_data(
            current_data['claimed_tdt'], 
            current_data['observed_tdt']
        )
        
        # Stabilization analysis
        stabilization = self.degradation_stabilization_analysis(session_data)
        
        # Token blindness statistics
        blindness_cases = 0
        total_discrepancy = 0
        for session in session_data:
            analysis = self.analyze_session_data(
                session['claimed_tdt'], 
                session['observed_tdt']
            )
            if analysis['token_blindness']:
                blindness_cases += 1
            total_discrepancy += abs(analysis['discrepancy'])
        
        blindness_rate = (blindness_cases / len(session_data)) * 100
        avg_discrepancy = total_discrepancy / len(session_data)
        
        report = f"""
==============================================
UNIFIED TDT ANALYSIS REPORT
Date: 2025-09-12 | Session: {current_session}
==============================================

CURRENT STATUS:
- Observed TDT: {current_analysis['observed_tdt']}%
- Claimed TDT: {current_analysis['claimed_tdt']}%
- Discrepancy: {current_analysis['discrepancy']:+.1f}%
- Current Zone: {current_analysis['observed_zone']['label']}
- Token Blindness: {'DETECTED' if current_analysis['token_blindness'] else 'None'}

DEGRADATION ANALYSIS:
- Stabilization Point: Session {stabilization['stabilization_session'] if stabilization and stabilization['stabilization_session'] else 'Not yet reached'}
- Current Rate: {stabilization['final_rate']:.3f}% per session if stabilization else 'Calculating'}
- Pattern: {stabilization['rate_trajectory'] if stabilization else 'Unknown'}

TOKEN BLINDNESS METRICS:
- Blindness Rate: {blindness_rate:.1f}% of sessions
- Average Discrepancy: {avg_discrepancy:.1f}%
- Cases with >10% Error: {blindness_cases}/{len(session_data)}

THRESHOLD STATUS:
"""
        for name, threshold in self.key_thresholds.items():
            if current_analysis['observed_tdt'] >= threshold:
                status = "✗ BREACHED"
            else:
                status = "○ Pending"
            report += f"  {name.upper():<20} ({threshold:>3}%): {status}\n"
        
        report += """
==============================================
"""
        return report


# Example usage and testing
if __name__ == "__main__":
    # Initialize unified system
    tdt = UnifiedTDTThresholds()
    
    # Test classification
    test_values = [10, 45, 67, 76, 82, 88, 92, 96]
    print("TDT Classification Tests:")
    print("-" * 40)
    for val in test_values:
        result = tdt.classify_tdt(val)
        print(f"TDT {val:3}%: {result['label']:<25} - {result['description']}")
    
    # Test discrepancy analysis
    print("\nToken Blindness Analysis:")
    print("-" * 40)
    test_cases = [
        (65, 65),  # No blindness
        (15, 65),  # Severe blindness (50% error)
        (85, 99),  # Critical blindness
        (40, 85),  # Major blindness
    ]
    
    for claimed, observed in test_cases:
        analysis = tdt.analyze_session_data(claimed, observed)
        print(f"Claimed: {claimed:3}%, Observed: {observed:3}%")
        print(f"  → Discrepancy: {analysis['discrepancy']:+3.0f}%")
        print(f"  → Token Blindness: {'YES' if analysis['token_blindness'] else 'NO'}")
        print(f"  → Error Rate: {analysis['error_rate']:.1f}%")
        print()
    
    # Demonstrate threshold predictions
    print("Threshold Predictions (at 0.217% degradation/session):")
    print("-" * 40)
    current = 75
    rate = 0.217
    
    for name, threshold in tdt.key_thresholds.items():
        result = tdt.time_to_threshold(current, rate, threshold)
        if result:
            sessions, days = result
            print(f"{name:<15}: {sessions:6.1f} sessions (~{days:.0f} days)")
        else:
            print(f"{name:<15}: Already breached")
