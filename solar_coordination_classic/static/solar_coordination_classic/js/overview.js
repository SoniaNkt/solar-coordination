const svgWidth = 1000;
const svgHeight = 800;

const svg = d3.select('.canvas')
    .append('svg')
    .attr('style', 'outline: thin solid #71797E;')
    .attr('width', svgWidth)
    .attr('height', svgHeight);

// Create margins and dimensions for the svg and the graph inside it

const margin = { top: 50, right: 50, bottom: 50, left: 50 };
const graphWidth = svgWidth - margin.left - margin.right;
const graphHeight = svgHeight - margin.top - margin.bottom;

// Create the graph and give it a margin

const entireGraph = svg.append('g')
    .attr('width', graphWidth)
    .attr('height', graphHeight)
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

// Create the graph axes
// const xAxisGroup = graph.append('g'); //x-axis not needed for this graph
const yAxisGroup = entireGraph.append('g')
    .attr('transform', `translate(0, 0)`); // Move the y-axis to the left

// Pull JSON data
d3.json('/fetch_solar_and_booked_values').then(json => {
    data = json.data
    console.log(data)

    const maxRectWidth = graphWidth - margin.right //largest bar padded on the right side

    const x = d3.scaleLinear() // Use a linear scale for x-axis
        .domain([0, d3.max(data, d => parseFloat(d.amount[0]))])
        .range([0, maxRectWidth]);

    const y = d3.scaleBand() // Use a band scale for y-axis
        .domain(data.map(item => item.hour))
        .range([0, graphHeight])
        .paddingInner(0.2)
        .paddingOuter(0.2);

    // Join data to rect groups
    const rects = entireGraph.selectAll('.rect-group')
        .data(data);

    const rectGroups = rects.enter()
        .append('g')
        .attr('class', 'rect-group')
        .attr('data-hour', d => d.hour)
        .attr('data-amount', d => d.amount[0]);

    rectGroups.append('rect')
        .attr('class', 'background-rect')  //class for the grey background rect
        .attr('data-hour', d => d.hour)
        .attr('data-amount', d => d.amount[0])
        .attr('width', d => graphWidth)
        .attr('height', y.bandwidth())
        .attr('fill', '#dcdcdc66')
        .attr('x', 1)
        .attr('y', d => y(d.hour));

    const yBandWidth = y.bandwidth()
    const yBandWidthBuffered = y.bandwidth() - 5

    rectGroups.append('rect')
        .attr('class', 'buffer-rect')  //class for the white buffer rect
        .attr('width', 20)
        .attr('height', yBandWidthBuffered)
        .attr('fill', 'white')
        .attr('x', 1)
        .attr('y', d => y(d.hour) + (yBandWidth - yBandWidthBuffered) / 2); //calculate the vertical position with some buffer

    rectGroups.append('rect')
        .attr('class', 'solar-rect')  //class for solar rect
        .attr('width', d => x(d.amount[0]))
        .attr('height', yBandWidthBuffered)
        .attr('fill', '#FFAE42')
        .attr('x', 20)
        .attr('y', d => y(d.hour) + (yBandWidth - yBandWidthBuffered) / 2); //calculate the vertical position with some buffer

    rectGroups.append('rect')
        .attr('class', 'booked-rect')  //class for booked rect
        .attr('width', d => x(d.amount[1]))
        .attr('height', yBandWidthBuffered)
        .attr('fill', '#444444')
        .attr('x', 20)
        .attr('y', d => y(d.hour) + (yBandWidth - yBandWidthBuffered) / 2); //calculate the vertical position with some buffer

    // provide rect-group solar data on hover
    rectGroups.on('mouseenter', function (event, d) {
        if (parseFloat(d.amount[0]) === 0) {
            const $this = $(this); // jQuery object for the clicked rect-group
            const popoverMsg = `No solar energy was generated at ${d.hour}`;
            $this.popover({
                trigger: 'hover',
                content: popoverMsg,
                placement: 'right',
            });
            $this.popover('show');
        } else if (parseFloat(d.amount[0]) > 0 && parseFloat(d.amount[1]) < parseFloat(d.amount[0])) {
            const $this = $(this);
            const popoverMsg = `Solar energy is available at ${d.hour}. Click to book.`;
            $this.popover({
                trigger: 'hover',
                content: popoverMsg,
                placement: 'right'
            });
            $this.popover('show');
        } else {
            const $this = $(this);
            const popoverMsg = `${d.hour} is fully booked.`;
            $this.popover({
                trigger: 'hover',
                content: popoverMsg,
                placement: 'right'
            });
            $this.popover('show');
        }
    }).on('mouseleave', function () {
        const $this = $(this);
        $this.popover('hide');
    });

    // click to book if solar is available    
    rectGroups.on('click', (event, d) => {
        if (parseFloat(d.amount[0]) > 0 && parseFloat(d.amount[1]) < parseFloat(d.amount[0])) {
            // Populate the hour input field in the modal
            $('#hourSelected').val(d.hour);

            $('#bookingModal').modal('show');
        }
    });

    $(document).ready(function () {
        $('[data-toggle="popover"]').popover();

        // Listen for changes in the 'activity' select field on the booking modal
        $('#selectedActivity').on('change', function () {
            const selectedActivity = $(this).val();
            const amount = $('#amount');

            // Update the 'amount' based on the selected option
            if (selectedActivity === 'Oven (2Hrs)') {
                amount.val(10);
            } else if (selectedActivity === 'Dishwasher (2Hrs)') {
                amount.val(2.5);
            } else if (selectedActivity === 'Washing Machine (3Hrs)') {
                amount.val(8);
            } else {
                amount.val('');
            }
        });
    });

    // Hide success/error elements when not called
    document.getElementById('success-alert').classList.add('d-none');
    document.getElementById('error-alert').classList.add('d-none');


    // Show the alert when success/error occurs
    function showSuccessAlert() {
        document.getElementById('success-alert').classList.remove('d-none');
    }

    function hideSuccessAlert() {
        document.getElementById('success-alert').classList.add('d-none');
    }

    function showErrorAlert() {
        document.getElementById('error-alert').classList.remove('d-none');
    }

    function hideErrorAlert() {
        document.getElementById('error-alert').classList.add('d-none');
    }

    $('#saveBooking').on('click', () => {
        const hour = $('#hourSelected').val();
        const selectedActivity = $('#selectedActivity').val();
        const amount = $('#amount').val();

        $.ajax({
            type: 'POST',
            url: '/create_booking/',
            data: {
                'name': selectedActivity,
                'hour': hour,
                'amount': amount,
                // csrfmiddlewaretoken: '{{ csrf_token }}'  // Include the CSRF token for security
            },
            success: function () {
                $('#bookingModal').modal('hide');
                showSuccessAlert();
                setTimeout(hideSuccessAlert, 15000);
            },
            error: function () {
                showErrorAlert();
                setTimeout(hideErrorAlert, 15000);
            }
        });
    });

    // Create and call the axes
    // const xAxis = d3.axisBottom(x); //x-axis not needed for this graph
    const yAxis = d3.axisLeft(y);

    // xAxisGroup.call(xAxis); //x-axis not needed for this graph
    yAxisGroup.call(yAxis);
});