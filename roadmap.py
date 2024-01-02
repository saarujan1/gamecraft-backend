class Roadmap:
    def __init__(self):
        self.milestones = []  # List to store milestones
        self.completion_status = []  # List to store the completion status of each milestone

    def add_milestone(self, milestone):
        self.milestones.append(milestone)
        self.completion_status.append(False)  # Initially, milestones are not complete

    def update_milestone_status(self, milestone, status):
        if milestone in self.milestones:
            index = self.milestones.index(milestone)
            self.completion_status[index] = status
        else:
            raise ValueError("Milestone does not exist")

    def get_milestone_status(self, milestone):
        if milestone in self.milestones:
            index = self.milestones.index(milestone)
            return self.completion_status[index]
        else:
            raise ValueError("Milestone does not exist")

    def __str__(self):
        return str(list(zip(self.milestones, self.completion_status)))

# Example:
roadmap = Roadmap()
roadmap.add_milestone("Prototype Complete")
roadmap.add_milestone("First Playable")
roadmap.add_milestone("Feature Complete")

# Update the status of a milestone to True indicating it's complete
roadmap.update_milestone_status("Prototype Complete", True)

print(roadmap) 