class PGxtraUtility:
    """Ideally, PGxtraUtility should be a singleton - i.e. only one such object
    can exist at any time. But for now, we will not enforce this - not until we
    arrive at a model that really works well.
    """
    def __init__(self):
        """Creates dictionary of all pgxtra control widgets, keyed by type."""
        self.widgets = {}

    def add_widget(self, widget):
        """Add the widget. Each widget is categorized by it's type."""
        self.widgets.setdefault(widget.__class__, []).append(widget)

    def get_widgets(self, widget_type=None):
        """Return all the widgets. If widget_type is not None, returns only
        the widgets of the specified type.
        """
        returnVal = []
        if widget_type <> None and widget_type in self.widgets:
            returnVal.extend(self.widgets[widget_type])
        else:
            for values in self.widgets.itervalues():
                returnVal.extend(values)
        return returnVal

def main():
    ## Basic tests
    util = PGxtraUtility()
    util.add_widget("foo")
    print util.get_widgets()

if __name__ == '__main__':
    main()
