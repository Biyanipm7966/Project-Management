// Array to store permanent events (hardcoded)
const permanentEvents = [
    {
        dateFrom: '09 / 24 / 2024',
        dateTo: '09 / 24 / 2024',
        description: 'Kickoff',
    },
    {
        dateFrom: '09 / 25 / 2024',
        dateTo: '10 / 08 / 2024',
        description: 'Brainstorming',
    },
    {
        dateFrom: '10 / 09 / 2024',
        dateTo: '10 / 29 / 2024',
        description: 'Development',
    },
    {
        dateFrom: '10 / 30 / 2024',
        dateTo: '11 / 12 / 2024',
        description: 'Testing and Quality Assurance',
    },
    {
        dateFrom: '11 / 13 / 2024',
        dateTo: '11 / 26 / 2024',
        description: 'Finalizing',
    },
    {
        dateFrom: '11 / 27 / 2024',
        dateTo: '11 / 27 / 2024',
        description: 'Release',
    },
];

// Array to store temporary events (in-memory)
let events = [];

// Current date to track displayed month and year
let currentMonth = new Date().getMonth(); // Starts at 0 (January)
let currentYear = new Date().getFullYear();

// Render the calendar
function renderCalendar() {
    const calendar = document.querySelector('.calendar');
    const monthYear = document.querySelector('#month-year');

    // Clear previous calendar content
    calendar.innerHTML = '';

    // Display the current month and year
    const date = new Date(currentYear, currentMonth);
    monthYear.innerText = date.toLocaleDateString('en-US', {
        month: 'long',
        year: 'numeric',
    });

    // Get the first day of the month and number of days in the month
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Add blank spaces for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const blankCell = document.createElement('div');
        blankCell.classList.add('calendar-day', 'blank');
        calendar.appendChild(blankCell);
    }

    // Add days to the calendar
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.classList.add('calendar-day');
        dayCell.innerText = day;

        const formattedDate = `${currentYear}-${currentMonth + 1}-${day}`;

        // Check for permanent and temporary events on this day
        const dayPermanentEvents = permanentEvents.filter((event) =>
            isDateInRange(formattedDate, event.dateFrom, event.dateTo)
        );
        const dayTemporaryEvents = events.filter((event) =>
            isDateInRange(formattedDate, event.dateFrom, event.dateTo)
        );

        // Display event indicators for both types of events
        if (dayPermanentEvents.length > 0 || dayTemporaryEvents.length > 0) {
            const totalEvents = dayPermanentEvents.length + dayTemporaryEvents.length;
            const eventIndicator = document.createElement('div');
            eventIndicator.classList.add('event-indicator');
            eventIndicator.innerText = `${totalEvents} events`;
            dayCell.appendChild(eventIndicator);
        }

        // Add event listener for viewing events
        dayCell.addEventListener('click', () => openEventModal(currentYear, currentMonth, day));

        calendar.appendChild(dayCell);
    }
}

// Check if a date is within a range
function isDateInRange(date, dateFrom, dateTo) {
    const targetDate = new Date(date);
    const startDate = new Date(dateFrom);
    const endDate = new Date(dateTo);

    return targetDate >= startDate && targetDate <= endDate;
}

// Open the event modal
function openEventModal(year, month, day) {
    const modal = document.querySelector('#event-modal');
    const eventDateDisplay = document.querySelector('#event-date-display');
    const eventList = document.querySelector('#event-list');
    const eventDescription = document.querySelector('#event-description');
    const eventDateFrom = document.querySelector('#event-date-from');
    const eventDateTo = document.querySelector('#event-date-to');

    const selectedDate = `${month + 1} / ${day} / ${year}`;
    eventDateDisplay.innerText = selectedDate;

    modal.style.display = 'flex';

    // Get events for the selected date
    const dayPermanentEvents = permanentEvents.filter((event) =>
        isDateInRange(selectedDate, event.dateFrom, event.dateTo)
    );
    const dayTemporaryEvents = events.filter((event) =>
        isDateInRange(selectedDate, event.dateFrom, event.dateTo)
    );

    // Display existing events (both permanent and temporary)
    eventList.innerHTML = ''; // Clear the existing event list
    [...dayPermanentEvents, ...dayTemporaryEvents].forEach((event, index) => {
        const eventItem = document.createElement('div');
        eventItem.classList.add('event-item');
        eventItem.innerHTML = `
            <span>${event.description} (${event.dateFrom} - ${event.dateTo})</span>
            ${
                dayPermanentEvents.includes(event)
                    ? '' // No delete button for permanent events
                    : `<button class="delete-event" data-index="${index}" data-date-from="${event.dateFrom}" data-date-to="${event.dateTo}">Delete</button>`
            }
        `;
        eventList.appendChild(eventItem);
    });

    // Add delete functionality for temporary events
    const deleteButtons = document.querySelectorAll('.delete-event');
    deleteButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const dateFrom = this.getAttribute('data-date-from');
            const dateTo = this.getAttribute('data-date-to');
            deleteEvent(dateFrom, dateTo);
        });
    });

    // Save new event
    const saveButton = document.querySelector('#save-event');
    saveButton.onclick = function () {
        const description = eventDescription.value;
        const dateFrom = eventDateFrom.value;
        const dateTo = eventDateTo.value;

        if (description && dateFrom && dateTo) {
            events.push({ dateFrom, dateTo, description });
            modal.style.display = 'none';
            renderCalendar(); // Re-render the calendar with the new event
        }
    };

    const closeButton = document.querySelector('#close-modal');
    closeButton.onclick = function () {
        modal.style.display = 'none';
    };
}

// Delete a temporary event
function deleteEvent(dateFrom, dateTo) {
    // Remove the specific event from the main events array
    events = events.filter(
        (event) => !(event.dateFrom === dateFrom && event.dateTo === dateTo)
    );

    // Re-render the calendar
    renderCalendar();
}

// Navigate to the previous month
function prevMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
}

// Navigate to the next month
function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar();
}

// Initial render
renderCalendar();

// Attach navigation event listeners
document.querySelector('#prev-month').addEventListener('click', prevMonth);
document.querySelector('#next-month').addEventListener('click', nextMonth);