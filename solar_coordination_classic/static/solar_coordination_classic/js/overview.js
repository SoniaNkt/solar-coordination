const svgWidth = 800;
const svgHeight = 800;

const svg = d3.select('.canvas')
    .append('svg')
    .attr('style', 'outline: thin solid black;')
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

$(document).ready(function () {
    $('[data-toggle="popover"]').popover();
});

// Pull JSON data
d3.json('/fetch_solar_values').then(json => {
    data = json.data
    console.log(data)

    const maxRectWidth = graphWidth - margin.right //largest bar padded on the right side

    const x = d3.scaleLinear() // Use a linear scale for x-axis
        .domain([0, d3.max(data, d => parseFloat(d.amount))])
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
        .attr('data-amount', d => d.amount);

    rectGroups.append('rect')
        .attr('class', 'background-rect')  //class for the grey background rect
        .attr('data-hour', d => d.hour)
        .attr('data-amount', d => d.amount)
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
        .attr('width', d => x(d.amount))
        .attr('height', yBandWidthBuffered)
        .attr('fill', '#FFAE42')
        .attr('x', 20)
        .attr('y', d => y(d.hour) + (yBandWidth - yBandWidthBuffered) / 2); //calculate the vertical position with some buffer

    rectGroups.append('rect')
        .attr('class', 'booked-rect')  //class for booked rect
        .attr('width', d => 5)
        .attr('height', yBandWidthBuffered)
        .attr('fill', '#444444')
        .attr('x', 20)
        .attr('y', d => y(d.hour) + (yBandWidth - yBandWidthBuffered) / 2); //calculate the vertical position with some buffer


    // click to book if solar is available    
    rectGroups.on('click', (event, d) => {
        if (parseFloat(d.amount) > 0) {
            const modalHour = document.getElementById('hourSelected');
            const modalAmount = document.getElementById('amountSelected');
            modalHour.textContent = `Hour: ${d.hour}`;
            modalAmount.textContent = `Amount: ${d.amount}`;
            $('#bookingModal').modal('show');
        }
    });

    // provide rect-group solar data on hover
    rectGroups.on('mouseenter', function (event, d) {
        if (parseFloat(d.amount) === 0) {
            const $this = $(this); // jQuery object for the clicked rect-group
            const popoverMsg = `No solar power was generated at ${d.hour}`;
            $this.popover({
                trigger: 'hover',
                content: popoverMsg,
                placement: 'right',
            });
            $this.popover('show'); // Show the popover
        } else {
            const $this = $(this);
            const popoverMsg = `Solar power is available at ${d.hour}. Click to book.`;
            $this.popover({
                trigger: 'hover',
                content: popoverMsg,
                placement: 'right'
            });
            $this.popover('show');
        }
    }).on('mouseleave', function () {
        const $this = $(this);
        $this.popover('hide'); // Hide popover when mouse leaves
    });

    // Create and call the axes
    // const xAxis = d3.axisBottom(x); //x-axis not needed for this graph
    const yAxis = d3.axisLeft(y);

    // xAxisGroup.call(xAxis); //x-axis not needed for this graph
    yAxisGroup.call(yAxis);
});