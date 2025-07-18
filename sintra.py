import argparse
import sys
import json
from measurement_client.client import SintraMeasurementClient
from measurement_client.logger import logger
from event_manager.eventmanager import SintraEventManager

def main():
    parser = argparse.ArgumentParser(description='Sintra Network Measurement & Event Management Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Measurement commands
    create_parser = subparsers.add_parser('create', help='Create measurements')
    create_parser.add_argument('--config', help='Configuration file path (overrides default)')
    
    fetch_parser = subparsers.add_parser('fetch', help='Fetch measurement results')
    fetch_parser.add_argument('--config', help='Configuration file path (overrides default)')
    fetch_parser.add_argument('--measurement-id', type=int, help='Specific measurement ID to fetch')
    
    # Event management commands
    detect_parser = subparsers.add_parser('detect', help='Detect anomalies in measurement results')
    alerts_parser = subparsers.add_parser('alerts', help='Show alerts summary')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'create':
            client = SintraMeasurementClient(config_path=args.config)
            client.create_measurements()
            
        elif args.command == 'fetch':
            client = SintraMeasurementClient(config_path=args.config)
            client.fetch_measurements(args.measurement_id)
        
        elif args.command == 'detect':
            event_manager = SintraEventManager()
            event_manager.analyze_all()
            logger.info("Anomaly detection complete. Alerts have been stored in event_manager/results/<measurement_id>.json.")

        elif args.command == 'alerts':
            event_manager = SintraEventManager()
            for result_file in event_manager.event_results_dir.glob("*.json"):
                with open(result_file, "r") as f:
                    data = json.load(f)
                measurement_id = data.get("measurement_id")
                events = data.get("events", [])
                logger.info(f"Measurement {measurement_id}: {len(events)} anomalies detected.")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
