let fill = d3.scaleOrdinal(d3.schemeBlues[7]);

colors = ['#003f77', '#0062bb', '#1c69ad', '#2f5579', '#b9e0ff', '#ffffff']

let data = [
    {text: "Осень на дворе", value: 1000},
    {text: "безлюдным", value: 2000},
    {text: "очень болен", value: 2000},
    {text: "ночь", value: 4000},
    {text: "Черный", value: 4000},
    {text: "невмочь", value: 4000},
    {text: "Друг мой", value: 6000},
    {text: "Черный человек", value: 6000}];

let layout

function drawCloud(data){
    for (let i = 0; i < data.length; i++){
        data[i] = {text: data[i][0], value: (i+1)*500+1000}
    }
    layout = d3.layout.cloud()
        .size([600, 600])
        .words(data)
        .padding(5)
        .font("Mulish")
        .rotate(function () {
            return ~~(Math.random() * 12 - 6) * 10;
        })
        .on("end", draw);
    layout.start()
}
function draw(words) {
    d3.select("#cloud")
        .append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .text((d) => d.text)
        .style("font-family", (d) => d.font)
        .style("fill", (d, i) => "#00000000")
        .attr("class", "title")
        .attr("text-anchor", "middle")
        .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")")
        .on('click', (e, d) => {
            cleanLayout();
            titleSelected(d.text);
        })
        .transition()
        .ease(d3.easeLinear)
        .duration(2000)
        .delay(1000)
        .attr("font-size", (d) => d.size + "px")
        .style("fill", (d, i) => colors[i]);
}


function cleanLayout() {
    d3.select("#cloud")
        .selectAll("text")
        .transition()
        .ease(d3.easeLinear)
        .duration(1000)
        .attr("font-size", "1px")
        .style("fill", (d, i) => "#00000000");
    setTimeout(() => d3.selectAll("svg > *").remove(), 3000)
}


