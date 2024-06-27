import os

class QAEfficiencyCalculator:
    def __init__(self, dev_count, qa_count, dev_output_per_week, defect_rate, qa_capacity_per_week):
        self.dev_count = dev_count
        self.qa_count = qa_count
        self.dev_output_per_week = dev_output_per_week
        self.defect_rate = defect_rate
        self.qa_capacity_per_week = qa_capacity_per_week

    def calculate(self):
        total_code_output = self.dev_count * self.dev_output_per_week
        total_defects = total_code_output * self.defect_rate
        total_qa_capacity = self.qa_count * self.qa_capacity_per_week
        defect_detection_efficiency = total_qa_capacity / total_code_output

        return {
            'total_code_output': total_code_output,
            'total_defects': total_defects,
            'total_qa_capacity': total_qa_capacity,
            'defect_detection_efficiency': defect_detection_efficiency
        }

    def generate_dot_file(self, results, filename="sdlc_efficiency.dot"):
        total_code_output = results['total_code_output']
        total_defects = results['total_defects']
        total_qa_capacity = results['total_qa_capacity']
        efficiency = results['defect_detection_efficiency']

        efficiency_color = "green" if efficiency >= 1 else "orange" if efficiency >= 0.5 else "red"

        dot_content = f"""
        digraph SDLC_Efficiency {{
            rankdir=LR;
            node [shape=box, style=filled, color=lightblue2];

            dev_team [label="Development Team\\nSize: {self.dev_count}", shape=ellipse];
            qa_team [label="QA Team\\nSize: {self.qa_count}", shape=ellipse];
            dev_output [label="Total Code Output\\n{total_code_output} units/week"];
            defects [label="Total Defects\\n{total_defects} defects/week"];
            qa_capacity [label="Total QA Capacity\\n{total_qa_capacity} units/week"];
            efficiency [label="Defect Detection Efficiency\\n{efficiency:.2f}", shape=ellipse, color={efficiency_color}];

            dev_team -> dev_output [label="produces"];
            dev_output -> defects [label="results in"];
            qa_team -> qa_capacity [label="can handle"];
            qa_capacity -> efficiency [label="affects"];
            defects -> efficiency [label="affects"];
        }}
        """

        with open(filename, "w") as file:
            file.write(dot_content)
        print(f"DOT file generated: {filename}")

if __name__ == "__main__":
    dev_count = 20
    qa_count = 6
    dev_output_per_week = 50  # units of code
    defect_rate = 0.1  # defects per unit of code
    qa_capacity_per_week = 200  # units of code

    calculator = QAEfficiencyCalculator(dev_count, qa_count, dev_output_per_week, defect_rate, qa_capacity_per_week)
    results = calculator.calculate()
    calculator.generate_dot_file(results)

    # Generate visualization using Graphviz (requires Graphviz installed)
    os.system("dot -Tpng sdlc_efficiency.dot -o sdlc_efficiency.png")
    print("Visualization generated: sdlc_efficiency.png")
