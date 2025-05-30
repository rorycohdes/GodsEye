"use client";

import { useEffect, useRef } from "react";
import * as d3 from "d3";
import styles from "./ForceDirectedGraph.module.css";

export default function ForceDirectedGraph() {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear any existing SVG content
    d3.select(svgRef.current).selectAll("*").remove();

    // Sample data for the graph
    const nodes = [
      { id: "Node 1", group: 1 },
      { id: "Node 2", group: 1 },
      { id: "Node 3", group: 1 },
      { id: "Node 4", group: 2 },
      { id: "Node 5", group: 2 },
      { id: "Node 6", group: 3 },
      { id: "Node 7", group: 3 },
      { id: "Node 8", group: 3 },
      { id: "Node 9", group: 3 },
      { id: "Node 10", group: 4 },
    ];

    const links = [
      { source: "Node 1", target: "Node 2", value: 1 },
      { source: "Node 2", target: "Node 3", value: 1 },
      { source: "Node 2", target: "Node 4", value: 1 },
      { source: "Node 3", target: "Node 5", value: 1 },
      { source: "Node 5", target: "Node 6", value: 1 },
      { source: "Node 6", target: "Node 7", value: 1 },
      { source: "Node 7", target: "Node 8", value: 1 },
      { source: "Node 8", target: "Node 9", value: 1 },
      { source: "Node 9", target: "Node 10", value: 1 },
      { source: "Node 1", target: "Node 10", value: 1 },
      { source: "Node 2", target: "Node 8", value: 1 },
      { source: "Node 3", target: "Node 6", value: 1 },
      { source: "Node 4", target: "Node 7", value: 1 },
    ];

    // Get the dimensions of the container
    const svgElement = svgRef.current;
    const width = svgElement.clientWidth;
    const height = svgElement.clientHeight;

    // Create a color scale
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // Create a force simulation
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(width / 2).strength(0.1))
      .force("y", d3.forceY(height / 2).strength(0.1));

    // Create the SVG container
    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");

    // Add zoom functionality
    const g = svg.append("g");
    svg.call(
      d3
        .zoom()
        .extent([
          [0, 0],
          [width, height],
        ])
        .scaleExtent([0.1, 8])
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
        })
    );

    // Create the links
    const link = g
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", (d) => Math.sqrt(d.value));

    // Create the nodes
    const node = g
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 10)
      .attr("fill", (d) => color(d.group))
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

    // Add titles (tooltips)
    node.append("title").text((d) => d.id);

    // Add labels to the nodes
    const labels = g
      .append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .attr("font-size", "10px")
      .attr("fill", "#fff")
      .text((d) => d.id);

    // Update positions on each tick of the simulation
    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

      labels.attr("x", (d) => d.x).attr("y", (d) => d.y);
    });

    // Drag functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup function
    return () => {
      simulation.stop();
    };
  }, []);

  return (
    <div className={styles.graphContainer}>
      <div className={styles.header}>
        <h1>Force Directed Graph</h1>
        <p>Interactive network visualization using D3.js</p>
      </div>
      <div className={styles.graphWrapper}>
        <svg ref={svgRef} className={styles.graph}></svg>
      </div>
    </div>
  );
}
