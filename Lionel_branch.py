import calendar
from datetime import datetime

class Schedule:
    def __init__(self):
        self.shifts_data = {} # Will store the shifts data

    def update_shift(self, caregivers):
        """Assign shifts based on caregiver availability and preferences."""
        self.shifts_data.clear() #Clear the existing shift data
        shifts = ["7AM - 1PM", "1PM - 7PM", "7PM - 7AM"]
        days_in_month = range(1, 32) # Have to define the fays in a month. Going to use 31 days

        for day in days_in_month:
            for shift_time in shifts:
                available_caregivers = [cg for cg in caregivers if self.is_available(cg, shift_time)] #Find caregivers who are available for the shift
                if available_caregivers:
                    available_caregivers.sort(key=lambda cg: self.get_preference(cg, shift_time), reverse=True) #Sort caregivers by their preference for the shift
                    caregiver = available_caregivers[0]
                    self.shifts_data.setdefault(day, []).append((caregiver.name, shift_time))

    def is_available(self, caregiver, shift_time):
        """Check if caregiver is available for a shift.""" # Check if the caregiver is available for the shift time
        for shift in caregiver.shifts:
            if shift_time in shift and caregiver.shifts[shift] != "Unavailable":
                return True
        return False

    def get_preffered_shifts(self, caregivers, shift_time):
        """Get caregivers who prefer a shift.""" # Have to check if the caregiver prefers the shift
        for shift in caregivers.shifts:
            if shift["shift"] == shift_time:
                return shift ["availability"] == "Preferred"
        return False

    def generate_calendar_view(self): # Initialize the calendar string with the month and year

        """Generate a calendar view of the shifts.""" # Get the current month and year
        current_month = datetime.now().month 
        current_year = datetime.now().year
        cal = calendar.Calendar(calendar.SUNDAY)
        cal_month = cal.monthdayscalendar(current_year, current_month) # Get days of the current month in a matrix format

        calendar_str = f"{calendar.month_name[current_month]} {current_year}\n"
        calendar_str += "Sun  Mon  Tue  Wed  Thu  Fri  Sat\n"
        for week in cal_month:
            week_str = ""
            for day in week: # Loop through the days of the week
                if day != 0: 
                    shifts_for_day = "\n".join([f"{caregiver}: {shift}" for caregiver, shift in self.shifts_data.get(day, [])]) # Get the shifts for the day
                    if shifts_for_day:
                        week_str += f"{day:2} ({shifts_for_day})  "
                    else:
                        week_str += f"{day:2} (No shifts)  " # If there are no shifts for the day
                else:
                    week_str += "    " # Add the spaces for the days that are not in the month
            
            calendar_str += week_str + "\n"

        return calendar_str # Return the calendar string