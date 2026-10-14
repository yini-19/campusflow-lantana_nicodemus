from campusflow.tickets import (
    create_ticket,
    list_tickets,
    view_ticket,
)
from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_work_queue,
    reopen_ticket,
)
from campusflow.reports import generate_report
from campusflow.storage import load_tickets, save_tickets


def display_menu():
    print("""
    ==============================
        CAMPUS WORKFLOW
    ==============================
        1. CREATE TICKET
        2. LIST ALL TICKETS
        3. VIEW TICKET
        4. ASSIGN TICKET TO STAFF
        5. CHANGE STATUS
        6. WORK QUEUE
        7. REPORTS
        8. REOPEN TICKET
        9. ADD FOLLOW-UP NOTES
       10. VIEW TICKET NOTES
       11. EXIT
    ==============================
    """)


def main():
    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return

    while True:
        display_menu()
        choice = input("Select action: ").strip()

        try:
            if choice == "1":
                create_ticket(tickets)
                save_tickets(tickets)

            elif choice == "2":
                list_tickets(tickets)

            elif choice == "3":
                view_ticket(tickets)

            elif choice == "4":
                ticket_id = input("Ticket ID: ").strip().upper()
                staff_name = input("Staff name: ")

                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets)
                print("Ticket assigned successfully.")

            elif choice == "5":
                ticket_id = input("Ticket ID: ").strip().upper()
                new_status = input(
                    "New status (in_progress/resolved): "
                )

                change_status(tickets, ticket_id, new_status)
                save_tickets(tickets)
                print("Ticket status updated successfully.")

            elif choice == "6":
                queue = get_work_queue(tickets)

                if not queue:
                    print("No unresolved tickets.")
                else:
                    for ticket in queue:
                        print(
                            f'{ticket["id"]} | '
                            f'{ticket["priority"]} | '
                            f'{ticket["title"]} | '
                            f'{ticket["status"]}'
                        )

            elif choice == "7":
                report = generate_report(tickets)

                print(f'Total tickets: {report["total_tickets"]}')
                print("Status breakdown:")

                for status, count in report["status_breakdown"].items():
                    print(f"  {status}: {count}")

                print("Priority breakdown:")

                for priority, count in report["priority_breakdown"].items():
                    print(f"  {priority}: {count}")

            elif choice == "8":
                ticket_id = input("Ticket ID: ").strip().upper()

                reopen_ticket(tickets, ticket_id)
                save_tickets(tickets)
                print("Ticket reopened successfully.")

            elif choice == "9":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Select an option between 1 and 9.")

        except (ValueError, OSError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()