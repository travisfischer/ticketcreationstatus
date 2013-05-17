from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener
from trac.config import Option

class TicketCreationStatus(Component):
    implements(ITicketChangeListener)

    default_status = Option('ticketcreationstatus', 'default', None,
        doc="""Determines the status for tickets (if not otherwise modified).""")

    owned_status = Option('ticketcreationstatus', 'owned', None,
        doc="""Determines the status for tickets that start out owned.""")

    type_defaults_status = Option('ticketcreationstatus', 'type_defaults', None,
        doc="""Determines the status for tickets of a certain type.""")

    def ticket_created(self, ticket):
        status = None

        if self.type_defaults_status:
            type_status_map = {}
            mappings = self.type_defaults_status.split(',')
            for mapping in mappings:
                ticket_type, ticket_status = mapping.split('->')
                type_status_map[ticket_type.strip()] = ticket_status.strip()

            status = type_status_map.get(ticket['type'], None)

        if not status and self.owned_status:
            if ticket['owner']:
                status = self.owned_status

        if not status and self.default_status:
            status = self.default_status

        if status is not None:
            ticket['status'] = status
            ticket.save_changes()

    def ticket_changed(self, ticket, comment, author, old_values):
        pass

    def ticket_deleted(self, ticket):
        pass
