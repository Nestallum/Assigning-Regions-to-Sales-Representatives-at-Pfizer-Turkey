# Assigning-Regions-to-Sales-Representatives-at-Pfizer-Turkey

## Work Description

The project consists of the following tasks:

- **Describe the situation and the decision problem** (stakeholders, issues, data, etc.).
- **Specify the set of choices** and the evaluation criteria.
- **Compute efficient solutions**.
- **Discriminate solutions using an additive model**.
- **Analyze the limitations** of the proposed model.

## Key Questions

Address the following questions:

1. **Solution properties**: Do the obtained solutions have properties that are worth bringing to the attention of the decision maker?
2. **Comparison of solutions**: Discuss the properties of the current solution in comparison to the solutions you have obtained.
3. **Varying workload**: Varying workload is currently modeled as a constraint. Try modifying this constraint (e.g., using the interval [0.9, 1.1]), and discuss how it affects the solution set and trade-offs with other goals.
4. **Partial assignment of bricks**: How can the model handle partial assignment of bricks (i.e., assigning a brick to multiple sales representatives)? Implement this and compare the results.
5. **Increased demand**: If demand increases uniformly (e.g., +20%), it may be necessary to hire a new sales representative. Discuss where to locate their office (center brick).
6. **Location of center bricks**: The location of the SR offices (center bricks) impacts travel distances. How can the model be generalized to modify the center bricks? This requires additional binary variables. Note that some bricks may not be suitable as center bricks, reducing the number of variables.
7. **SR preferences**: How can the model incorporate the sales representatives' preferences for their assigned areas?

## Tools

Choose an appropriate **solver/modeler** to implement the solution.
