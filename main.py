from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView

from jnius import autoclass

ContactsContract = autoclass('android.provider.ContactsContract')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class ContactList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

class CallGate(App):

    def build(self):
        self.allowed = set()
        layout = BoxLayout(orientation='vertical')

        self.search = TextInput(
            hint_text="Search contact",
            size_hint_y=None,
            height=100
        )
        self.search.bind(text=self.filter_contacts)

        self.rv = ContactList()
        self.contacts = self.load_contacts()
        self.update_list(self.contacts)

        layout.add_widget(self.search)
        layout.add_widget(self.rv)
        return layout

    def load_contacts(self):
        activity = PythonActivity.mActivity
        resolver = activity.getContentResolver()

        cursor = resolver.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            None, None, None, None
        )

        results = []
        while cursor.moveToNext():
            name = cursor.getString(
                cursor.getColumnIndex(
                    ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME
                )
            )
            number = cursor.getString(
                cursor.getColumnIndex(
                    ContactsContract.CommonDataKinds.Phone.NUMBER
                )
            )
            results.append({"text": f"{name} : {number}"})

        cursor.close()
        return results

    def update_list(self, items):
        self.rv.data = items

    def filter_contacts(self, instance, value):
        filtered = [
            c for c in self.contacts
            if value.lower() in c["text"].lower()
        ]
        self.update_list(filtered)

CallGate().run()
