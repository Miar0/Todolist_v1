import calendar


class Task:
    def __init__(self, title, deadline, status):
        self.title = title
        self.deadline = deadline
        self.status = status

    def get_color_day(self, current_datetime, cal):
        day = self.deadline.day
        month = self.deadline.month
        year = self.deadline.year

        diff_year = current_datetime.year != year
        equals_month = current_datetime.month == month
        less_than_cm = month < current_datetime.month
        less_than_cy = year < current_datetime.year
        less_or_equals_cd = day <= current_datetime.day

        if ((less_than_cy and diff_year) or (less_than_cm and less_than_cy) or (equals_month and less_or_equals_cd and not diff_year)) and \
                self.status is False:
            cal.calevent_create(self.deadline, self.title, "code_red")
            cal.tag_config("code_red", background="red", foreground="white")

        elif (not less_than_cm and not less_or_equals_cd) and self.status is False:
            if equals_month:
                days = day - current_datetime.day
            else:
                days_in_cm = calendar.monthrange(current_datetime.year, current_datetime.month)[1]
                days = (days_in_cm - current_datetime.day) + day
            if days <= 3:
                cal.calevent_create(self.deadline, self.title, "code_orange")
                cal.tag_config("code_orange", background="orange", foreground="white")
            elif days <= 5:
                cal.calevent_create(self.deadline, self.title, "code_gold")
                cal.tag_config("code_gold", background="gold", foreground="white")
            elif days > 5:
                cal.calevent_create(self.deadline, self.title, "code_blue")
                cal.tag_config("code_blue", background="blue", foreground="white")
        elif self.status is True:
            cal.calevent_create(self.deadline, self.title, "code_green")
            cal.tag_config("code_green", background="green", foreground="white")
        else:
            cal.calevent_create(self.deadline, self.title, "code_blue")
            cal.tag_config("code_blue", background="blue", foreground="white")
